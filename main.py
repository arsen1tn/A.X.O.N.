from axon.core.application import Application
from axon.core.logger import logger
from axon.ai.ai_service import AIService
from axon.core.Chat_service import Chat_service
from axon.ai.providers.hybrid_provider import HybridProvider
from axon.services.web_service import WebService
from axon.skills.skill_manager import SkillManager


provider = HybridProvider(gemini_api_key="a")
ai_service = AIService(provider=provider)

def main():
    app = Application()
    skills = SkillManager()
    skills.load_skills()
    chat_service = Chat_service(ai_service=ai_service, app=app)
    app.register_service(chat_service)
    web_service = WebService(hybrid_provider=provider, skill_manager=skills)
    app.register_service(web_service)
                             
    app.run()
    #chat_service.run_chat()
    app.wait()
    app.stop()
        
if __name__ == "__main__":
    main()