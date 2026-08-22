from collections import defaultdict
from typing import Any, Callable, Dict, List
from axon.core.logger import logger

class EventBus:
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = defaultdict(list)
        
    def subscribe(self, event_name: str, callback: Callable) -> None:
        self._subscribers[event_name].append(callback)
        logger.debug(f"Subscribed '{callback.__name__}' to '{event_name}'")
    
    def emit(self, event_name: str, *args, **kwargs) -> None:
        for callback in self._subscribers.get(event_name, []):
            try:
                callback(*args, **kwargs)
            except Exception as e:
                logger.error(f"Error in  '{callback.__name__}' for '{event_name}': {e}")
                    