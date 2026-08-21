from abc import ABC, abstractmethod
from axon.core.logger import logger

class BaseService(ABC):
    """Base class for all A.X.O.N. services."""
    
    def __init__(self, name: str):
        self.name = name
        self.is_running = False
        

    @abstractmethod
    def start(self) -> bool:
        pass
    
    @abstractmethod
    def stop(self) -> bool:
        pass