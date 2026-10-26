from threading import Lock
from typing import Dict, List, Optional


class ContextManager:
    def __init__(self, max_messages: Optional[int] = None, store=None):
        self.max_messages = max_messages
        self.store = store
        self._history: List[Dict[str, str]] = []
        self._lock = Lock()

        if self.store:
            self._history = self.store.load_messages()

    def add_message(self, role: str, content: str) -> None:
        with self._lock:
            self._history.append({"role": role, "content": content})
            if self.store:
                self.store.save_message(role, content)
            if self.max_messages is not None and len(self._history) > self.max_messages:
                self._history = self._history[-self.max_messages:]

    def get_history(self, limit: Optional[int] = None) -> List[Dict[str, str]]:
        with self._lock:
            if limit is None:
                return list(self._history)
            if limit <= 0:
                return []
            return list(self._history[-limit:])

    def clear_history(self) -> None:
        with self._lock:
            self._history.clear()
            if self.store:
                self.store.clear()