import os
import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from typing import TypedDict, NotRequired
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnablePassthrough


class LLMSettings(TypedDict):
    provider: str
    model: str
    temperature: NotRequired[float]
    
def get_openrouter_models(provider: dict) -> list[str]:
    return [
        "meta-llama/llama-3-70b",
        
        
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

PROVIDERS = {
    "openrouter": {
        "base_url": os.environ.get("OPENROUTER_API_BASE"),
        "api_key": os.environ.get("OPENROUTER_API_KEY"),
        "models_loader": get_openrouter_models,
    }
}

if __name__ == "__main__":

    load_dotenv()
    settings = LLMSettings(
        provider="openrouter",
        model="meta-llama/llama-3-70b",
        temperature=0.5
    )


    prompt = "Tell me a short joke about {topic}"
    output_parser = StrOutputParser()
    model = get_llm_client(settings)
    
    chain = (
    {"topic": RunnablePassthrough()} 
    | prompt
    | model
    | output_parser
    )
    
    
    res =chain.invoke("ice cream")
    print(res)