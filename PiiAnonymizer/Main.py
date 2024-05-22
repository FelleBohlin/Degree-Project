import os
import time
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from LLMSettings import LLMSettings

# Gets the available models 
def get_openrouter_models(provider: dict) -> list[str]:
    return [
        "meta-llama/llama-3-70b-instruct",
        "qwen/qwen-110b-chat",
        "meta-llama/llama-3-8b-instruct"
        
    ]

# Initialize and return an LLM client with the given settings.
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

# Load environment variables from a .env file
load_dotenv()

# Get the OpenRouter API key from the environment variables
OPENROUTER_API_KEY = os.environ["OPENROUTER_API_KEY"]
if OPENROUTER_API_KEY is None:
    raise ValueError("OPENROUTER_API_KEY does not exist, add it to env")

# Defines the PROVIDERS dictionary with configuration details for each provider
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
        Numeriskt Identifierare - Alla numeriska eller alfanumeriska identifierare som ärendenummer, medlemsnummer, biljettnummer, bankkontonummer, IP-adresser, produktnycklar, serienummer, spårningsnummer för frakt, etc.in
        Kreditkort - Alla kreditkortsnummer, säkerhetskoder eller utgångsdatum.

    Texten som ska anonymizeras:

    {text}
    """)

    # Prompt template for the second chain
    # Used to focus on the detection and anonymization of names
    names_prompt_template = ChatPromptTemplate.from_template("""
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

    # Prompt template for the third chain
    # Used to generate dummy data
    dummy_data_prompt_template = ChatPromptTemplate.from_template("""
    Du är en författare.
    Din uppgift är att ersätta alla [ANONYMIZED] taggar i texten med påhittad data som passar in i sammanhanget.
    Byt ut varje [ANONYMIZED] tagg mot en realistisk och kontextuell entitet.
    Byt endast ut dessa taggar, ingenting annat. Skriv inga förklaringar eller sammanfattningar, ersätt endast [ANONYMIZED] taggar. 

    Exempel på hur texten ska ersättas:
    'Jag träffade en person som hette [ANONYMIZED] igår'. -> 'Jag träffade en person som hette Johan igår'
    'Jag träffade en person som hette [ANONYMIZED] igår. Han gav mig sitt telefonnummer [ANONYMIZED] samt hans e-postadress [ANONYMIZED].' -> 'Jag träffade en person som hette Erik igår. Han gav mig sitt telefonnummer 070-123-4567 samt hans e-postadress erik.exempel@mail.com.'
'Min vän [ANONYMIZED] bor på [ANONYMIZED]. Hennes IP-adress är [ANONYMIZED].' -> 'Min vän Lisa bor på Storgatan 22. Hennes IP-adress är 192.168.0.1.'
    

    Texten som ska bearbetas:

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
    names_chain = (
        names_prompt_template
        | model_second
        | output_parser
    )

    # Third chain: generates dummy data
    dummy_data_chain = (
        dummy_data_prompt_template
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
        if filename.endswith(".txt") and os.path.isfile(input_filepath):  # Ensure the file ends with .txt to avoid permission deneid errors
            output_filepath = os.path.join(output_dir, filename)

            with open(input_filepath, 'r', encoding='utf-8') as file:
                input_text = file.read()
    
            # Run the first chain
            first_result = anonymize_chain.invoke({"text": input_text})
            first_text = first_result.strip()
    
            # Run the second chain with the output of the first chain
            second_result = names_chain.invoke({"text": first_text})
            second_text = second_result.strip()

            # Run the third chain with the output of the second chain to generate dummy data.
            final_result = dummy_data_chain.invoke({"text": second_text})
            final_text = final_result.strip()
            
            # Write the final anonymized text to the output file
            with open(output_filepath, 'w', encoding='utf-8') as file:
                file.write(final_text)

    end_time = time.time()
    elapsed_time = end_time - start_time

    # Prints a confirmation that the anonymizaation process is complete
    # Prints how long it took to anonymize the input directory
    print(f"Anonymization process completed in {elapsed_time:.2f} seconds.")



PROVIDERS = {
    "openrouter": {
        "base_url": os.environ["OPENROUTER_API_BASE"],
        "api_key": os.environ["OPENROUTER_API_KEY"],
        "models_loader": get_openrouter_models,
    },
    "ollama": {
        "base_url": os.environ["LLM_API_BASE"],
        "api_key": "ollama",
        "models_loader": get_ollama_models,
    },
    "vllm": {
        "base_url": os.environ["VLLM_API_BASE"],
        "api_key": "vllm",
        "models_loader": get_vllm_models,
    },
}
