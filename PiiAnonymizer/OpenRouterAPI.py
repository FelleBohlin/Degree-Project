# openrouter_api.py
import requests
import json

class OpenRouterAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"

    def request_completion(self, prompt):
                # Ensure prompt is a plain string
        if hasattr(prompt, 'text'):
            prompt_text = prompt.text
        else:
            prompt_text = str(prompt)
            
        response = requests.post(
            url=self.base_url, 
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }, 
            data=json.dumps({
                "model": "meta-llama/llama-3-70b",
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            })
        )

        if response.status_code == 200:
            response_data = response.json()
            return response_data['choices'][0]['message']['content']
        else:
            raise Exception(f"API request failed with status code {response.status_code}: {response.text}")

    def __call__(self, prompt):
        return self.request_completion(prompt)
