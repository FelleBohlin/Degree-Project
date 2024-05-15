from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from OpenRouterAPI import OpenRouterAPI
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser

def create_first_chain(api_key):
    # First prompt template
    first_prompt_template = """
    test
    """
    
    first_prompt = PromptTemplate(
        input_variables=["text"], template=first_prompt_template
    )
    
    # Initialize the LLM for the first stage using OpenRouterAPI
    first_llm = OpenRouterAPI(api_key)
    return first_prompt | first_llm | StrOutputParser()