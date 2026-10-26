import sqlite3
from contextlib import closing
from pathlib import Path
 
DEFAULT_DB_PATH = Path(__file__).parent.parent / "memory" / "axon_memory.db"
 
 
class MemoryStore:
    def __init__(self, db_path=DEFAULT_DB_PATH):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._create_table()
 
    def _connect(self):
        return sqlite3.connect(self.db_path)
 
    def _create_table(self):
        with closing(self._connect()) as conn:
            with conn:
                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS messages (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        role TEXT NOT NULL,
                        content TEXT NOT NULL,
                        created_at TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                    """
                )
 
    def save_message(self, role: str, content: str) -> None:
        with closing(self._connect()) as conn:
            with conn:
                conn.execute(
                    "INSERT INTO messages (role, content) VALUES (?, ?)",
                    (role, content),
                )
 
    def load_messages(self, limit: int = None) -> list:
        with closing(self._connect()) as conn:
            if limit is None:
                rows = conn.execute(
                    "SELECT role, content FROM messages ORDER BY id"
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT role, content FROM "
                    "(SELECT id, role, content FROM messages ORDER BY id DESC LIMIT ?) "
                    "ORDER BY id",
                    (limit,),
                ).fetchall()
        return [{"role": role, "content": content} for role, content in rows]
 
    def clear(self) -> None:
        with closing(self._connect()) as conn:
            with conn:
                conn.execute("DELETE FROM messages")