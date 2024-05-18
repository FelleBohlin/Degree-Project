from langchain_core.runnables import RunnableSequence
from langchain_core.prompts import PromptTemplate
from OpenRouterAPI import OpenRouterAPI
from langchain_core.output_parsers import StrOutputParser

def create_first_chain(api_key):
    # First prompt template
    first_prompt_template = """
    Du är en säkerhetsassistent.
    Din uppgift är att identifiera och anonymisera all personligt identifierbar information (PII).
    När du hittar PII, ersätt den med '[ANONYMIZED]'. Anonymisera endast texten, skriv ingenting annat. Skriv inga förklaringar eller sammanfattningar, endast anonymiserad text.

    Exempel på hur texten ska anonymiseras:
    'Jag träffade en person som hette Johan Svensson igår. Han gav mig sitt telefonnummer 123-456-7890 samt hans e-postadress johan.svensson@gmail.com.' ->
    'Jag träffade en person som hette [ANONYMIZED] igår. Han gav mig sitt telefonnummer [ANONYMIZED] samt hans e-postadress [ANONYMIZED].'
    'Min vän Maria bor på Storgatan 1, 12345 Stockholm. Hennes IP-adress är 192.168.1.1.' ->
    'Min vän [ANONYMIZED] bor på [ANONYMIZED]. Hennes IP-adress är [ANONYMIZED].'
    'Kundens kreditkortsnummer är 1234-5678-9876-5432 med utgångsdatum 12/23.' ->
    'Kundens kreditkortsnummer är [ANONYMIZED] med utgångsdatum [ANONYMIZED].'

    Personlig känslig information (PII) inkluderar:
        Person/Namn - Detta inkluderar förnamn, mellannamn, efternamn eller hela namn på individer (inklusive enskilda förnamn eller efternamn, inte bara fullständiga namn).
        Telefonnummer - Alla telefonnummer, inklusive avgiftsfria nummer.
        Adress - Kompletta eller partiella adresser, inklusive gata, postnummer, husnummer, stad och stat.
        E-post - Alla e-postadresser.
        Numeriskt Identifierare - Alla numeriska eller alfanumeriska identifierare som ärendenummer, medlemsnummer, biljettnummer, bankkontonummer, IP-adresser, produktnycklar, serienummer, spårningsnummer för frakt, etc.
        Kreditkort - Alla kreditkortsnummer, säkerhetskoder eller utgångsdatum.

    Anonymisera följande text:
    """
    
    prompt = PromptTemplate(input_variables=["text"], template=first_prompt_template)
    llm = OpenRouterAPI(api_key)
    parser = StrOutputParser()

    return RunnableSequence(prompt, llm, parser)

