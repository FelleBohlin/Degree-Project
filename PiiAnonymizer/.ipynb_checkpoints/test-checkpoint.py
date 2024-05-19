import os
import json
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
        "base_url": "https://openrouter.ai/api/v1",
        "api_key": "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",
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

    # Prompt templates
    anonymize_prompt_template = ChatPromptTemplate.from_template("Anonymize all PII in the following text: {text}")
    emphasize_names_prompt_template = ChatPromptTemplate.from_template("Make sure the following text has no names mentioned and emphasize anonymization of names: {text}")

    # Output parsers
    output_parser = StrOutputParser()

    # LLM client
    model = get_llm_client(settings)

    # First chain: Anonymize all PII
    anonymize_chain = (
        RunnableMap({"text": RunnablePassthrough()})
        | anonymize_prompt_template
        | model
        | output_parser
    )

    # Second chain: Emphasize anonymization of names
    emphasize_names_chain = (
        RunnableMap({"text": RunnablePassthrough()})
        | emphasize_names_prompt_template
        | model
        | output_parser
    )

    # Input text
    input_text = "John Doe, a software engineer at Acme Corp, lives at 123 Elm Street."

    # Run the first chain
    anonymized_text = anonymize_chain.invoke({"text": input_text})

    # Run the second chain with the output of the first chain
    final_result = emphasize_names_chain.invoke({"text": anonymized_text})

    print(final_result)
