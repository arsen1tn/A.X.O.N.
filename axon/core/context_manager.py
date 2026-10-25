from threading import Lock
from typing import Any, Dict, List, Optional
 
 
class ContextManager:
    def __init__(self, max_messages: Optional[int] = None):
        self._data: Dict[str, Any] = {}
        self._history: List[dict] = []
        self._max_messages = max_messages
        self._lock = Lock()
 
    def set(self, key: str, value: Any) -> None:
        with self._lock:
            self._data[key] = value
 
    def get(self, key: str, default: Optional[Any] = None) -> Any:
        with self._lock:
            return self._data.get(key, default)
 
    def add_message(self, role: str, content: str) -> None:
        with self._lock:
            self._history.append({"role": role, "content": content})
            if self._max_messages is not None and len(self._history) > self._max_messages:
                self._history = self._history[-self._max_messages:]
 
    def get_history(self, limit: Optional[int] = None) -> List[dict]:
        with self._lock:
            if limit is None:
                return list(self._history)
            return self._history[-limit:]
 
    def clear_history(self) -> None:
        with self._lock:
            self._history = []