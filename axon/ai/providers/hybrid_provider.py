from axon.ai.providers.base import BaseLLMProvider
from axon.ai.providers.openai_provider import OpenAIProvider
import socket

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
            socket.create_connection(("8.8.8.8", 53), timeout=2)
            return True
        except OSError:
            return False
    
    def generate(self, prompt: str) -> str:
        complex_prompt = self._is_complex(prompt)
        cloud = self.smart_provider if complex_prompt else self.fast_provider

        if self._has_internet() or complex_prompt:
            try:
                print(f"☁️ [Gemini] {cloud.model}")
                return cloud.generate(prompt)
            except Exception as e:
                print(e)
                print("🧠 [Ollama]")
                return self.local_provider.generate(prompt)
        else:
            print("🧠 [Ollama]")
            return self.local_provider.generate(prompt)