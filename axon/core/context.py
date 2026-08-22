from typing import Any, Dict, Optional
from threading import Lock
from axon.core.logger import logger

class ContextManager:
    def __init__(self):
        self.__data: Dict[str, Any] = {}
        self.__lock = Lock()
    
    def set(self, key: str, value: Any) -> None:
        with self.__lock:
            self.__data[key] = value
            logger.debug(f"Context set: {key} = {value}")

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        with self.__lock:
            return self.__data.get(key, default)