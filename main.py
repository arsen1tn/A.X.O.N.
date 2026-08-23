from axon.core.application import Application
from axon.core.dummy_service import DummyService
from axon.core.logger import logger
from axon.ai.ai_service import AIService

def main():
    app = Application()
    app.register_service(AIService())
    app.register_service(DummyService())
    
    try:
        app.run()
        app.wait()
    except KeyboardInterrupt:
        logger.info("Received interrupt signal. Shutting down...")
    finally:
        app.stop()
        
if __name__ == "__main__":
    main()