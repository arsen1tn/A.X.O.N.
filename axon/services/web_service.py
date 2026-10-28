import threading
import time
import webbrowser
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn
from axon.core.logger import logger

HTML_FILE_PATH = Path(__file__).parent / "index.html"


class ChatMessage(BaseModel):
    message: str
    chat_id: Optional[str] = None


class NewChat(BaseModel):
    title: str = "New chat"


class RenameChat(BaseModel):
    title: str


class WebService:
    def __init__(self, hybrid_provider, skill_manager, host="0.0.0.0", port=8000):
        self.name = "WebService"
        self.hybrid_provider = hybrid_provider
        self.skill_manager = skill_manager
        self.host = host
        self.port = port

        self.app = FastAPI(title="AXON Web Service")
        self.server = None
        self.server_thread = None
        self.is_running = False

        self.setup_routes()

    def _require_chat(self, chat_id: str):
        if not self.context.chat_exists(chat_id):
            raise HTTPException(status_code=404, detail="Chat not found")

    def _chat_label(self, chat_id: str) -> str:
        # "Chat title | a1b2c3d4" for log lines
        for chat in self.context.list_chats():
            if chat["id"] == chat_id:
                return f"{chat['title']} | {chat_id[:8]}"
        return chat_id[:8]

    def _learn_facts(self, message: str, label: str):
        # Runs in a background thread, so the reply is not delayed
        try:
            known = self.context.get_facts()
            for fact in self.hybrid_provider.extract_facts(message, known):
                if self.context.add_fact(fact):
                    logger.info(f"[{label}] New fact saved: {fact}")
        except Exception as e:
            logger.warning(f"Fact learning failed: {e}")

    def setup_routes(self):
        @self.app.get("/", response_class=FileResponse)
        async def read_root():
            if not HTML_FILE_PATH.exists():
                raise HTTPException(status_code=404, detail="Index file not found")
            return FileResponse(HTML_FILE_PATH)

        # ---------- chats ----------

        @self.app.get("/api/chats")
        def list_chats():
            return {"chats": self.context.list_chats()}

        @self.app.post("/api/chats")
        def create_chat(body: NewChat):
            return self.context.create_chat(body.title)

        @self.app.patch("/api/chats/{chat_id}")
        def rename_chat(chat_id: str, body: RenameChat):
            self._require_chat(chat_id)
            self.context.rename_chat(chat_id, body.title)
            return {"ok": True}

        @self.app.delete("/api/chats/{chat_id}")
        def delete_chat(chat_id: str):
            self._require_chat(chat_id)
            self.context.delete_chat(chat_id)
            return {"ok": True}

        @self.app.get("/api/chats/{chat_id}/messages")
        def chat_messages(chat_id: str):
            self._require_chat(chat_id)
            return {"messages": self.context.get_history(chat_id)}

        # ---------- shared facts ----------

        @self.app.get("/api/facts")
        def list_facts():
            return {"facts": self.context.list_facts()}

        @self.app.delete("/api/facts/{fact_id}")
        def delete_fact(fact_id: int):
            self.context.delete_fact(fact_id)
            return {"ok": True}

        # ---------- sending a message ----------

        @self.app.post("/api/chat")
        def chat_endpoint(request: ChatMessage):
            message = request.message

            # No chat given -> start a new one. Unknown chat -> 404.
            chat_id = request.chat_id
            if not chat_id:
                chat_id = self.context.create_chat()["id"]
            else:
                self._require_chat(chat_id)

            self.context.add_message(chat_id, "user", message)

            # The first message of a chat becomes its title
            if len(self.context.get_history(chat_id)) == 1:
                self.context.rename_chat(chat_id, message.strip()[:40] or "New chat")

            label = self._chat_label(chat_id)
            logger.info(f"[{label}] User: {message}")

            skill_reply = self.skill_manager.handle(message)
            if skill_reply is not None:
                self.context.add_message(chat_id, "assistant", skill_reply)
                logger.info(f"[{label}] AXON (skill): {skill_reply}")
                return {"response": skill_reply, "chat_id": chat_id}

            history = self.context.get_history(chat_id)
            facts = self.context.get_facts()
            reply = self.hybrid_provider.generate(message, history=history, facts=facts)

            self.context.add_message(chat_id, "assistant", reply)
            logger.info(f"[{label}] AXON: {reply}")

            threading.Thread(
                target=self._learn_facts, args=(message, label), daemon=True
            ).start()

            return {"response": reply, "chat_id": chat_id}

    def run(self):
        config = uvicorn.Config(
            app=self.app,
            host=self.host,
            port=self.port,
            log_level="info",
            access_log=False,
        )
        self.server = uvicorn.Server(config)
        self.server.install_signal_handlers = lambda: None
        self.server.run()

    def start(self):
        if self.is_running:
            logger.info("Web Service is already running.")
            return False

        self.is_running = True

        self.server_thread = threading.Thread(target=self.run, daemon=True)
        self.server_thread.start()
        time.sleep(0.5)

        if self.server_thread.is_alive():
            local_url = f"http://127.0.0.1:{self.port}"

            logger.info("Web Service is running!")
            logger.info(f"Open on other devices: http://26.240.165.88:{self.port}")

            try:
                webbrowser.open(local_url)
            except Exception as e:
                logger.error(f"Failed to open web browser: {e}")

            return True
        else:
            logger.error("Failed to start Web Service.")
            self.is_running = False
            return False

    def stop(self):
        if self.is_running and self.server:
            logger.info("Stopping Web Service...")
            self.server.should_exit = True
            self.is_running = False
            logger.info("Web Service has been stopped.")