from abc import ABC, abstractmethod

class BaseLLMProvider(ABC):
    
   @abstractmethod
   
   def generate(self, prompt: str, history=None) -> str:
            pass