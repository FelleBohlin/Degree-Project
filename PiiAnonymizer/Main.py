# main.py
import os
from dotenv import load_dotenv
from First_prompt import create_first_chain
from Second_prompt import create_second_chain
from langchain.chains import SimpleSequentialChain

# Load API key from environment variables
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
if api_key is None:
    raise ValueError("OPENROUTER_API_KEY does not exist, add it to env")

def anonymize_text(text, api_key):
    # Create chains
    first_chain = create_first_chain(api_key)
    second_chain = create_second_chain(api_key)
    
    # Run combined chain
    first_result = first_chain.invoke({"text": text})
    second_result = second_chain.invoke({"text": first_result["text"]})
    return second_result["text"]

if __name__ == "__main__":
    input_text = """
    Under en kaffe på ett mysigt café i Stockholm träffade jag Johan Svensson. 
    Anna delade med sig av sin e-postadress anna.svensson@gmail.com och sitt telefonnummer 070-1234567 så att vi kunde hålla kontakten. 
    Hon nämnde också att hon bor på Storgatan 1, 12345 Stockholm. 
    Anna är projektledare och berättade att hon nyligen fått ett nytt jobb hos sitt nya företag. 
    Dessutom pratade hon om sitt senaste onlineköp där hon använde sitt kreditkort 1234-5678-9876-5432, med utgångsdatum 12/23 och säkerhetskoden 123.
    """

    anonymized_text = anonymize_text(input_text, api_key)
    print(anonymized_text)
