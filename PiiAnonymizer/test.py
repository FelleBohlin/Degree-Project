import os
import json
import time
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence, RunnableMap
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from typing import TypedDict, NotRequired
from langchain_core.runnables import RunnablePassthrough
from llm_settings import LLMSettings

def get_openrouter_models(provider: dict) -> list[str]:
    return [
        "meta-llama/llama-3-70b-instruct",
        "qwen/qwen-110b-chat",
        "meta-llama/llama-3-8b-instruct"
        
    ]

def get_llm_client(settings: LLMSettings) -> ChatOpenAI:
    model = settings["model"]
    provider = PROVIDERS[settings["provider"]]

    options = {
        "base_url": provider["base_url"],
        "api_key": provider["api_key"],
        "model": model,
        "temperature": settings.get("temperature", 0.0)
    }
    return ChatOpenAI(**options)



load_dotenv()

OPENROUTER_API_KEY = os.environ["OPENROUTER_API_KEY"]
if OPENROUTER_API_KEY is None:
    raise ValueError("OPENROUTER_API_KEY does not exist, add it to env")
    
PROVIDERS = {
    "openrouter": {
        "base_url": "https://openrouter.ai/api/v1",
        "api_key": os.getenv("OPENROUTER_API_KEY"),
        "models_loader": get_openrouter_models,
    }
}

if __name__ == "__main__":
    
    settings_first_model = LLMSettings(
        provider="openrouter",
        model="meta-llama/llama-3-70b-instruct",
        temperature=0.5
    )

    settings_second_model = LLMSettings(
        provider="openrouter",
        model="meta-llama/llama-3-8b-instruct",
        temperature=0.5
    )
    
    # Prompt template for the first chain.
    # Used to detect and anonymize all PII
    anonymize_prompt_template = ChatPromptTemplate.from_template("""
    Du är en säkerhetsassistent.
    Din uppgift är att identifiera all personligt identifierbar information (PII).
    När du hittar PII, anonymizera den med denna tag [ANONYMIZED], som i exemplen nedan.
    Anonymizera endast texten med den taggen, skriv ingenting annat. Skriv inga förklaringar eller sammanfattningar, endast anonymizera texten.

    Exempel på hur texten ska anonymizeras:
    'Jag träffade en person som hette [ANONYMIZED] igår. Han gav mig sitt telefonnummer [ANONYMIZED] samt hans e-postadress [ANONYMIZED]'
    'Min vän [ANONYMIZED] bor på [ANONYMIZED]. Hennes IP-adress är [ANONYMIZED].'

    Personlig känslig information (PII) inkluderar:
        Person/Namn - Detta inkluderar förnamn, mellannamn, efternamn eller hela namn på individer (inklusive enskilda förnamn eller efternamn, inte bara fullständiga namn.).
        Telefonnummer - Alla telefonnummer, inklusive avgiftsfria nummer.
        Adress - Kompletta eller partiella adresser, inklusive gata, postnummer, husnummer, stad och stat.
        E-post - Alla e-postadresser.
        Numeriskt Identifierare - Alla numeriska eller alfanumeriska identifierare som ärendenummer, medlemsnummer, biljettnummer, bankkontonummer, IP-adresser, produktnycklar, serienummer, spårningsnummer för frakt, etc.
        Kreditkort - Alla kreditkortsnummer, säkerhetskoder eller utgångsdatum.

    Texten som ska anonymizeras:

    {text}
    """)

    # Prompt template for the second chain
    # Used to focus on the detection and anonymization of names
    emphasize_names_prompt_template = ChatPromptTemplate.from_template("""
    Du är en säkerhetsassistent.
    Din uppgift är att identifiera samt anonymizera alla namn.
    När du hittar ett namn, anonymizera den med denna tag, [ANONYMIZED], som i exemplen nedan.
    Anonymizera endast texten med den taggen, skriv ingenting annat. Skriv inga förklaringar eller sammanfattningar, endast anonymizera texten.

    Exempel på hur texten ska anonymizeras:
    'Jag träffade en person som hette Gustaf igår'. -> 'Jag träffade en person som hette [ANONYMIZED] igår'
    'Anna och Alice spelar tillsammans i samma fotbolls lag' -> '[ANONYMIZED] och [ANONYMIZED] spelar tillsammans i samma fotbolls lag'

    Namn inkluderar förnamn, mellannamn, efternamn eller hela namn på individer.

    Texten som ska anonymizeras:

    {text}
    """)

    # Output parsers
    output_parser = StrOutputParser()

    # LLM clients
    model_first = get_llm_client(settings_first_model)
    model_second = get_llm_client(settings_second_model)

    # First chain: Anonymize all PII
    anonymize_chain = (
        anonymize_prompt_template
        | model_first
        | output_parser
    )

    # Second chain: Focuses on anonymization of names
    emphasize_names_chain = (
        emphasize_names_prompt_template
        | model_second
        | output_parser
    )

     # Input and output directories (Note when running from the parent path specify the path depending on from where it is ran)
    input_dir = "generated_texts" 
    output_dir = os.path.join('PiiAnonymizer/Anonymized_texts')
    os.makedirs(output_dir, exist_ok=True)


    start_time = time.time()

    # Process each file in the input folder
    for filename in os.listdir(input_dir):
        input_filepath = os.path.join(input_dir, filename)
        if filename.endswith(".txt") and os.path.isfile(input_filepath):  # Ensure the file ens with .txt to avoid permission deneid errors
            output_filepath = os.path.join(output_dir, filename)

            with open(input_filepath, 'r', encoding='utf-8') as file:
                input_text = file.read()
    
            # Run the first chain
            anonymized_result = anonymize_chain.invoke({"text": input_text})
            anonymized_text = anonymized_result.strip()
    
            # Run the second chain with the output of the first chain
            final_result = emphasize_names_chain.invoke({"text": anonymized_text})
            final_text = final_result.strip()
    
            # Write the final anonymized text to the output file
            with open(output_filepath, 'w', encoding='utf-8') as file:
                file.write(final_text)

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Anonymization process completed in {elapsed_time:.2f} seconds.")
