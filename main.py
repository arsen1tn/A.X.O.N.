from axon.core.application import Application
from axon.core.logger import logger
from axon.ai.ai_service import AIService
from axon.core.Chat_service import Chat_service
from axon.ai.providers.openai_provider import OpenAIProvider
from axon.ai.providers.hybrid_provider import HybridProvider

provider = HybridProvider(gemini_api_key="Abcd")
ai_service = AIService(provider=provider)
chat_service = Chat_service(ai_service=ai_service)

def main():
    app = Application()
    app.register_service(chat_service)
    
    try:
        app.run()
        chat_service.run_chat()
        app.wait()
    except KeyboardInterrupt:
        logger.info("Received interrupt signal. Shutting down...")
    finally:
        app.stop()
        
if __name__ == "__main__":
    main()