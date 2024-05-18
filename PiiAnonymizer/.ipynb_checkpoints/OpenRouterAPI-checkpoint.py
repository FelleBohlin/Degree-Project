import os
import requests
import json
from dotenv import load_dotenv
from langchain_core.runnables import Runnable, RunnableSequence
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

class OpenRouterAPI(Runnable):
    def __init__(self, model_name, api_key=None, base_url="https://openrouter.ai/api/v1/chat/completions"):
        self.model_name = model_name
        self.api_key = api_key
        self.base_url = base_url

    def invoke(self, inputs):
        if not isinstance(inputs, dict) or 'prompt' not in inputs:
            raise ValueError("Input must be a dictionary containing a 'prompt' key.")
        prompt = inputs['prompt']
        response = requests.post(
            url=self.base_url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            data=json.dumps({
                "model": self.model_name,
                "messages": [{"role": "user", "content": prompt}]
            })
        )
        if response.status_code == 200:
            response_data = response.json()
            return {"text": response_data['choices'][0]['message']['content']}
        else:
            raise Exception(f"API request failed with status code {response.status_code}")
