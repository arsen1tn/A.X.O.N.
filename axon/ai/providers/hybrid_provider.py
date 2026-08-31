from axon.ai.providers.base import BaseLLMProvider
from axon.ai.providers.openai_provider import OpenAIProvider

class HybridProvider(BaseLLMProvider):
    def __init__(self, gemini_api_key: str):
        self.local_provider = OpenAIProvider(api_key="ollama", base_url="http://localhost:11434/v1", model="qwen2.5:3b")
        self.cloud_provider = OpenAIProvider(api_key=gemini_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/", model="gemini-3.5-flash")
        
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
    
    def generate(self, prompt: str) -> str:
        is_complex_task = self._is_complex(prompt)
        
        if not is_complex_task:
            try:
                print("🧠 [Ollama]")
                return self.local_provider.generate(prompt)
            except Exception as e:
                print("☁️ [Gemini]")
                return self.cloud_provider.generate(prompt)
        else:
            try:
                print("☁️ [Gemini]")
                return self.cloud_provider.generate(prompt)
            except Exception as e:
                print("🧠 [Ollama]")
                return self.local_provider.generate(prompt)