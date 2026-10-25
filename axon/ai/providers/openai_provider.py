from axon.ai.providers.base import BaseLLMProvider
from openai import OpenAI
from datetime import datetime

class OpenAIProvider(BaseLLMProvider):
    def __init__(self, api_key: str, base_url: str, model: str, reasoning_effort: str = None):
        self.client = OpenAI(api_key=api_key, base_url=base_url, timeout=20, max_retries=3)
        self.model = model
        self.reasoning_effort = reasoning_effort

    def generate(self, prompt: str, reasoning_effort: str = None) -> str:
        now = datetime.now().strftime("%A, %d %B %Y, %H:%M")

        params = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": f"The current local date and time is {now}."},
                {"role": "user", "content": prompt},
            ],
        }

        effort = reasoning_effort or self.reasoning_effort
        if effort:
            params["reasoning_effort"] = effort

        response = self.client.chat.completions.create(**params)

        return response.choices[0].message.content