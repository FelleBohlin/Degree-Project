import os
from dotenv import load_dotenv
from First_prompt import create_first_chain
from Second_prompt import create_second_chain

def anonymize_text(text, api_key):
    first_chain = create_first_chain(api_key)
    second_chain = create_second_chain(api_key)

    try:
        # Preparing the dictionary with necessary keys for the first chain
        first_inputs = {"text": text, "prompt_template": first_chain[0].template}
        first_result = first_chain[1].invoke(first_inputs)

        # Preparing the dictionary for the second chain using the output from the first chain
        second_inputs = {"text": first_result['text'], "prompt_template": second_chain[0].template}
        second_result = second_chain[1].invoke(second_inputs)

        return second_result['text']
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None


if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("OPENROUTER_API_KEY")
    if api_key is None:
        raise ValueError("OPENROUTER_API_KEY does not exist, add it to env")

    input_text = """
    Under en kaffe på ett mysigt café i Stockholm träffade jag Johan Svensson. 
    Anna delade med sig av sin e-postadress anna.svensson@gmail.com och sitt telefonnummer 070-1234567 så att vi kunde hålla kontakten. 
    Hon nämnde också att hon bor på Storgatan 1, 12345 Stockholm. 
    Anna är projektledare och berättade att hon nyligen fått ett nytt jobb hos sitt nya företag. 
    Dessutom pratade hon om sitt senaste onlineköp där hon använde sitt kreditkort 1234-5678-9876-5432, med utgångsdatum 12/23 och säkerhetskoden 123.
    """

    anonymized_text = anonymize_text(input_text, api_key)
    print("Anonymized Text:", anonymized_text)
