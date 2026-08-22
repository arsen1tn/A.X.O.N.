from axon.core.logger import logger
from axon.core.server import BaseService


class DummyService(BaseService):
    def __init__(self):
        super().__init__(name="DummyService")

    def _on_ping(self, data: str) -> None:
        status = self.context.get("dummy_status", "Unknown")
        logger.info(f"DummyService received ping with data: {data}. Current status in context: {status}")

    def start(self) -> bool:
        logger.info(f"Starting {self.name}...")
        self.is_running = True
        
        if hasattr(self, "context") and self.context:
            self.context.set("dummy_status", "Active and waiting!")
            
        if hasattr(self, "events") and self.events:
                    self.events.subscribe("ping_event", self._on_ping)
                    self.events.emit("ping_event", "Hello from DummyService!")
                    
        return True

    def stop(self) -> bool:
        logger.info(f"Stopping {self.name}...")
        self.is_running = False
        return True