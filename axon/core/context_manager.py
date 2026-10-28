from threading import Lock
from typing import Dict, List, Optional

from axon.memory.memory_store import MemoryStore


class ContextManager:
    def __init__(self, max_messages: Optional[int] = None, store: Optional[MemoryStore] = None):
        # max_messages=None means unlimited, keep the full conversation
        self.max_messages = max_messages
        self.store = store or MemoryStore()
        self._histories: Dict[str, List[Dict[str, str]]] = {}
        self._lock = Lock()

    # ---------- internal ----------

    def _history_for(self, chat_id: str) -> List[Dict[str, str]]:
        # Load a chat from the database the first time it is used
        if chat_id not in self._histories:
            self._histories[chat_id] = self.store.load_messages(chat_id)
        return self._histories[chat_id]

    # ---------- messages (one history per chat) ----------

    def add_message(self, chat_id: str, role: str, content: str) -> None:
        with self._lock:
            history = self._history_for(chat_id)
            history.append({"role": role, "content": content})
            self.store.save_message(chat_id, role, content)
            if self.max_messages is not None and len(history) > self.max_messages:
                self._histories[chat_id] = history[-self.max_messages:]

    def get_history(self, chat_id: str, limit: Optional[int] = None) -> List[Dict[str, str]]:
        with self._lock:
            history = self._history_for(chat_id)
            if limit is None:
                return list(history)
            if limit <= 0:
                return []
            return list(history[-limit:])

    def clear_history(self, chat_id: str) -> None:
        with self._lock:
            self._histories[chat_id] = []
            self.store.clear_chat(chat_id)

    # ---------- chats ----------

    def create_chat(self, title: str = "New chat") -> dict:
        with self._lock:
            chat = self.store.create_chat(title)
            self._histories[chat["id"]] = []
            return chat

    def list_chats(self) -> List[dict]:
        with self._lock:
            return self.store.list_chats()

    def chat_exists(self, chat_id: str) -> bool:
        with self._lock:
            return self.store.chat_exists(chat_id)

    def rename_chat(self, chat_id: str, title: str) -> None:
        with self._lock:
            self.store.rename_chat(chat_id, title)

    def delete_chat(self, chat_id: str) -> None:
        with self._lock:
            self.store.delete_chat(chat_id)
            self._histories.pop(chat_id, None)

    # ---------- shared facts (same for every chat) ----------

    def add_fact(self, content: str) -> bool:
        with self._lock:
            return self.store.add_fact(content)

    def get_facts(self) -> List[str]:
        with self._lock:
            return self.store.get_facts()

    def list_facts(self) -> List[dict]:
        with self._lock:
            return self.store.list_facts()

    def delete_fact(self, fact_id: int) -> None:
        with self._lock:
            self.store.delete_fact(fact_id)

    def clear_facts(self) -> None:
        with self._lock:
            self.store.clear_facts()