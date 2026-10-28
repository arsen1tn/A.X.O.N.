import sqlite3
import uuid
from contextlib import closing
from pathlib import Path

# axon/core/memory_store.py -> axon/memory/axon_memory.db
DEFAULT_DB_PATH = Path(__file__).parent.parent / "memory" / "axon_memory.db"

NOW = "strftime('%Y-%m-%d %H:%M:%f', 'now')"


class MemoryStore:
    def __init__(self, db_path=DEFAULT_DB_PATH):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._create_tables()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _create_tables(self):
        with closing(self._connect()) as conn:
            with conn:
                conn.execute(
                    f"""
                    CREATE TABLE IF NOT EXISTS chats (
                        id TEXT PRIMARY KEY,
                        title TEXT NOT NULL,
                        created_at TEXT DEFAULT ({NOW}),
                        updated_at TEXT DEFAULT ({NOW})
                    )
                    """
                )
                conn.execute(
                    f"""
                    CREATE TABLE IF NOT EXISTS messages (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        chat_id TEXT NOT NULL,
                        role TEXT NOT NULL,
                        content TEXT NOT NULL,
                        created_at TEXT DEFAULT ({NOW})
                    )
                    """
                )
                conn.execute(
                    "CREATE INDEX IF NOT EXISTS idx_messages_chat ON messages (chat_id, id)"
                )
                conn.execute(
                    f"""
                    CREATE TABLE IF NOT EXISTS facts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        content TEXT NOT NULL UNIQUE,
                        created_at TEXT DEFAULT ({NOW})
                    )
                    """
                )

    # ---------- chats ----------

    def create_chat(self, title: str = "New chat") -> dict:
        chat_id = uuid.uuid4().hex
        with closing(self._connect()) as conn:
            with conn:
                conn.execute(
                    "INSERT INTO chats (id, title) VALUES (?, ?)", (chat_id, title)
                )
        return {"id": chat_id, "title": title}

    def list_chats(self) -> list:
        with closing(self._connect()) as conn:
            rows = conn.execute(
                "SELECT id, title FROM chats ORDER BY updated_at DESC, rowid DESC"
            ).fetchall()
        return [{"id": cid, "title": title} for cid, title in rows]

    def chat_exists(self, chat_id: str) -> bool:
        with closing(self._connect()) as conn:
            row = conn.execute(
                "SELECT 1 FROM chats WHERE id = ?", (chat_id,)
            ).fetchone()
        return row is not None

    def rename_chat(self, chat_id: str, title: str) -> None:
        with closing(self._connect()) as conn:
            with conn:
                conn.execute(
                    "UPDATE chats SET title = ? WHERE id = ?", (title, chat_id)
                )

    def delete_chat(self, chat_id: str) -> None:
        with closing(self._connect()) as conn:
            with conn:
                conn.execute("DELETE FROM messages WHERE chat_id = ?", (chat_id,))
                conn.execute("DELETE FROM chats WHERE id = ?", (chat_id,))

    # ---------- messages ----------

    def save_message(self, chat_id: str, role: str, content: str) -> None:
        with closing(self._connect()) as conn:
            with conn:
                conn.execute(
                    "INSERT INTO messages (chat_id, role, content) VALUES (?, ?, ?)",
                    (chat_id, role, content),
                )
                conn.execute(
                    f"UPDATE chats SET updated_at = {NOW} WHERE id = ?", (chat_id,)
                )

    def load_messages(self, chat_id: str, limit: int = None) -> list:
        with closing(self._connect()) as conn:
            if limit is None:
                rows = conn.execute(
                    "SELECT role, content FROM messages WHERE chat_id = ? ORDER BY id",
                    (chat_id,),
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT role, content FROM "
                    "(SELECT id, role, content FROM messages "
                    " WHERE chat_id = ? ORDER BY id DESC LIMIT ?) "
                    "ORDER BY id",
                    (chat_id, limit),
                ).fetchall()
        return [{"role": role, "content": content} for role, content in rows]

    def clear_chat(self, chat_id: str) -> None:
        with closing(self._connect()) as conn:
            with conn:
                conn.execute("DELETE FROM messages WHERE chat_id = ?", (chat_id,))

    # ---------- shared facts ----------

    def add_fact(self, content: str) -> bool:
        content = content.strip()
        if not content:
            return False
        with closing(self._connect()) as conn:
            with conn:
                cur = conn.execute(
                    "INSERT OR IGNORE INTO facts (content) VALUES (?)", (content,)
                )
        return cur.rowcount > 0

    def get_facts(self) -> list:
        with closing(self._connect()) as conn:
            rows = conn.execute("SELECT content FROM facts ORDER BY id").fetchall()
        return [row[0] for row in rows]

    def list_facts(self) -> list:
        with closing(self._connect()) as conn:
            rows = conn.execute("SELECT id, content FROM facts ORDER BY id").fetchall()
        return [{"id": fact_id, "content": content} for fact_id, content in rows]

    def delete_fact(self, fact_id: int) -> None:
        with closing(self._connect()) as conn:
            with conn:
                conn.execute("DELETE FROM facts WHERE id = ?", (fact_id,))

    def clear_facts(self) -> None:
        with closing(self._connect()) as conn:
            with conn:
                conn.execute("DELETE FROM facts")