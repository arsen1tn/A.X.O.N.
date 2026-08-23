from axon.ai.providers.base import BaseLLMProvider
from openai import OpenAI

class OpenAIProvider(BaseLLMProvider):
    def __init__(self, api_key: str, base_url: str, model: str):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model
        
    def generate(self, prompt: str) -> str:
        response = self.client.chat.completions.create(model=self.model, messages=[{"role": "user", "content": prompt}])
        
        return response.choices[0].message.content