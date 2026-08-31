from axon.ai.ai_service import AIService
from axon.core.logger import logger

class Chat_service:
    def __init__(self, ai_service: AIService, app):
        self.ai_service = ai_service
        self.app = app
        self.name = "ChatService"
        self.is_running = False
        
    def start(self) -> bool:
        self.is_running = True
        logger.info("--- A.X.O.N. Chat Service Started ---")
        
        return True
    
    def run_chat(self) -> bool:
        try:    
             while True:
                user_input = input("User: ")
                if user_input.lower() in ["exit", "quit"]:
                    logger.info("Exiting chat service.")
                    self.app.stop()
                    break
                        
                response = self.ai_service.generate_response(user_input)
                logger.info(f"AI: {response}")
        except Exception as e:
                logger.error(f"Chat error: {e}")
                
    def stop(self) -> bool:
        self.is_running = False
        logger.info("--- A.X.O.N. Chat Service Stopped ---")
        
        return True
            