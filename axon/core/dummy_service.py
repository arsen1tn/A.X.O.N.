from axon.core.logger import logger
from axon.core.server import BaseService

class DummyService(BaseService):
    def __init__(self):
        super().__init__("DummyService")
    
    def start(self) -> bool:
        logger.info(f"Starting {self.name}...")
        self.is_running = True
        return True
    def stop(self) -> bool:
        logger.info(f"Stopping {self.name}...")
        self.is_running = False
        return True