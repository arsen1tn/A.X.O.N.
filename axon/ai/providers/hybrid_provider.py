import json
import socket
from contextlib import closing

from axon.ai.providers.base import BaseLLMProvider
from axon.ai.providers.openai_provider import OpenAIProvider
from axon.core.logger import logger

FACT_EXTRACTION_PROMPT = (
    "You extract long-term facts about the USER from one chat message.\n"
    "Save only stable, personal facts that will still be useful in future chats: "
    "name, age, city, job, projects, skills, preferences, family, pets, goals.\n"
    "Do NOT save: questions, small talk, temporary things, facts about other people "
    "unless they are important to the user, or anything secret "
    "(passwords, API keys, card numbers, ID numbers).\n"
    "Write each fact in English as a short statement, for example "
    "\"The user's name is Arsen\" or \"The user is building a voice assistant called A.X.O.N.\".\n"
    "Do not repeat facts that are already known.\n"
    "Reply with ONLY a JSON array of strings, for example [\"fact one\", \"fact two\"]. "
    "If there is nothing worth saving, reply with []."
)


class HybridProvider(BaseLLMProvider):
    def __init__(self, gemini_api_key: str):
        base = "https://generativelanguage.googleapis.com/v1beta/openai/"
        self.local_provider = OpenAIProvider(api_key="ollama", base_url="http://localhost:11434/v1", model="qwen2.5:3b")
        self.fast_provider = OpenAIProvider(api_key=gemini_api_key, base_url=base, model="gemini-3.5-flash-lite", reasoning_effort="low")
        self.smart_provider = OpenAIProvider(api_key=gemini_api_key, base_url=base, model="gemini-3.5-flash", reasoning_effort="medium")

    def _is_complex(self, prompt: str) -> bool:
        complex_keywords = [
            # Русский
            "код", "пиши", "напиши", "программу", "алгоритм", "анализ", "сравни", "объясни", "реши",
            # Английский
            "code", "write", "program", "algorithm", "analysis", "compare", "explain", "solve", "create",
        ]

        if len(prompt) > 100:
            return True

        prompt_lower = prompt.lower()

        for word in complex_keywords:
            if word in prompt_lower:
                return True

        return False

    def _has_internet(self) -> bool:
        try:
            with closing(socket.create_connection(("8.8.8.8", 53), timeout=2)):
                return True
        except OSError:
            return False

    def generate(self, prompt, history=None, facts=None):
        if self._has_internet():
            provider = self.smart_provider if self._is_complex(prompt) else self.fast_provider
            try:
                return provider.generate(prompt, history=history, facts=facts)
            except Exception as e:
                logger.warning(f"Cloud provider failed, falling back to local: {e}")

        return self.local_provider.generate(prompt, history=history, facts=facts)

    # ---------- shared facts ----------

    def _parse_facts(self, raw: str) -> list:
        if not raw:
            return []
        start, end = raw.find("["), raw.rfind("]")
        if start == -1 or end <= start:
            return []
        try:
            data = json.loads(raw[start:end + 1])
        except ValueError:
            return []
        if not isinstance(data, list):
            return []

        facts = []
        for item in data:
            if isinstance(item, str):
                fact = item.strip()
                if fact and len(fact) <= 200:
                    facts.append(fact)
        return facts[:5]

    def extract_facts(self, user_message: str, known_facts=None) -> list:
        # Cloud only: a small local model is too weak for this, and it is slow.
        if not self._has_internet():
            return []

        known = "\n".join(f"- {fact}" for fact in (known_facts or [])) or "(none)"
        prompt = f"Already known facts:\n{known}\n\nUser message:\n{user_message}"

        try:
            raw = self.fast_provider.generate(prompt, system_prompt=FACT_EXTRACTION_PROMPT)
        except Exception as e:
            logger.warning(f"Fact extraction failed: {e}")
            return []

        return self._parse_facts(raw)