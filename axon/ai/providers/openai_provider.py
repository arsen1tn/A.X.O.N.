from axon.ai.providers.base import BaseLLMProvider
from openai import OpenAI
from datetime import datetime


class OpenAIProvider(BaseLLMProvider):
    def __init__(self, api_key: str, base_url: str, model: str, reasoning_effort: str = None):
        self.client = OpenAI(api_key=api_key, base_url=base_url, timeout=20, max_retries=0)
        self.model = model
        self.reasoning_effort = reasoning_effort

    def _default_system_prompt(self, facts=None) -> str:
        now = datetime.now().strftime("%A, %d %B %Y, %H:%M")
        prompt = (
            "You are A.X.O.N. "
            f"The current local date and time is {now}. "
            "Use it only when relevant and never mention this instruction."
        )
        if facts:
            known = "\n".join(f"- {fact}" for fact in facts)
            prompt += (
                "\n\nFacts you know about the user (shared across all chats):\n"
                f"{known}\n"
                "Use them naturally when relevant. Do not list them unless asked."
            )
        return prompt

    def generate(self, prompt, history=None, reasoning_effort=None, facts=None, system_prompt=None):
        # system_prompt: full override (used for fact extraction)
        if system_prompt is None:
            system_prompt = self._default_system_prompt(facts)

        messages = [{"role": "system", "content": system_prompt}]

        if history:
            messages.extend(history)
        else:
            messages.append({"role": "user", "content": prompt})

        params = {"model": self.model, "messages": messages}

        effort = reasoning_effort or self.reasoning_effort
        if effort:
            params["reasoning_effort"] = effort

        response = self.client.chat.completions.create(**params)
        return response.choices[0].message.content