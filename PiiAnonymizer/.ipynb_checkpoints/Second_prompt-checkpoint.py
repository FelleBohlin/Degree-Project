from langchain_core.runnables import RunnableSequence
from langchain_core.prompts import PromptTemplate
from OpenRouterAPI import OpenRouterAPI
from langchain_core.output_parsers import StrOutputParser

def create_second_chain(api_key):
    second_prompt_template = """
    Du är en säkerhetsassistent med fokus på att anonymisera namn.
    Din uppgift är att säkerställa att alla namn är anonymiserade i texten. När du hittar ett namn, ersätt det med '[ANONYMIZED]'.
    Anonymisera endast namn, skriv ingenting annat. Skriv inga förklaringar eller sammanfattningar, endast anonymiserad text.
    
    Exempel på hur texten ska anonymiseras:
    'Jag träffade anna igår.' -> 'Jag träffade [ANONYMIZED] igår.'
    'Min vän Kristoffer bor på [ANONYMIZED].' -> 'Min vän [ANONYMIZED] bor på [ANONYMIZED].'
    'Projektledaren Johan Knutsson berättade att...' -> 'Projektledaren [ANONYMIZED] berättade att...'
    
    Anonymisera följande text:
    """
    
    # Create a PromptTemplate instance with the second prompt template
    prompt = PromptTemplate(input_variables=["text"], template=second_prompt_template)

    # Create an instance of the OpenRouterAPI with the provided API key
    llm = OpenRouterAPI(api_key)

    # Create an instance of StrOutputParser to parse the output text
    parser = StrOutputParser()

    # Return a RunnableSequence that chains the prompt, llm, and parser
    return RunnableSequence(prompt, llm, parser)