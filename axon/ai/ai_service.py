from axon.core.logger import logger
from axon.core.service import BaseService
from axon.ai.providers.base import BaseLLMProvider

class AIService(BaseService):
    def __init__(self, provider: BaseLLMProvider):
        super().__init__(name="AIService")
        self.provider = provider
        
    def start(self):
        self.is_running = True
        logger.info(f"Starting {self.name}")
    
        if hasattr(self, "events"):
            self.events.subscribe("user_input", self._on_user_input)
            
        return True    
    def _on_user_input(self, data: str):
        result = self.generate_response(data)
        logger.info(f"Response: {result}")

    def stop(self):
        self.is_running = False
        logger.info(f"Stopping {self.name}")
        return True
    
    def generate_response(self, prompt: str) -> str:
        logger.info(f"Generating response for: {prompt}")
        return self.provider.generate(prompt)