from axon.core.state import AppState
from axon.core.logger import logger, setup_logger
from axon.core.config import Config
from axon.core.lifecycle import Lifecycle
from axon.core.server import BaseService
import time

class Application:
    """
    Main application class.

    Coordinates all A.X.O.N. modules.
    """

    VERSION = "0.1.0"

    def __init__(self):
        self.running = False
        self.state = AppState.CREATED
        self.config = Config()
        self.lifecycle = Lifecycle()
        self.services = []
    
    def register_service(self, service: BaseService) -> None:
        self.services.append(service)
        logger.info(f"Registered service: {service.name}")
               
    def run(self):
        self.running = True
        
        setup_logger()
        
        self.lifecycle.set_state(AppState.STARTING)
        
        if not self.config.load():
            logger.error("Failed to load configuration.")
            self.lifecycle.set_state(AppState.ERROR)
            self.stop()
            return
        self.lifecycle.set_state(AppState.INITIALIZING)
        
        app_name = self.config.get("application.name", "A.X.O.N.")
        app_version = self.config.get("application.version", "0.1.0")
        logger.info("=" * 50)
        logger.info(f"{app_name} v{app_version}")
        logger.info("=" * 50)
        logger.info("Initializing Core...")
        logger.info("Loading Configuration...")
        logger.info("Starting Services...")
        
        for service in self.services:
            if not service.start():
                logger.error(f"Failed to start service: {service.name}")
                        
        self.lifecycle.set_state(AppState.READY)
        self.lifecycle.set_state(AppState.RUNNING)
        
        logger.info("✔ Core initialized.")
        logger.info("✔ Ready.")
                
    def wait(self):
        while self.running:
            time.sleep(1)
            
    def stop(self):
        self.lifecycle.set_state(AppState.STOPPING)
        logger.info("Stopping A.X.O.N...")
        
        for service in reversed(self.services):
            if service.is_running:
                service.stop()
                
        self.lifecycle.set_state(AppState.STOPPED)
        logger.info("✔ A.X.O.N. stopped.")
        