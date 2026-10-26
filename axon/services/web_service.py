import threading
import time
import webbrowser
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn
from axon.core.logger import logger
 
HTML_FILE_PATH = Path(__file__).parent / "index.html"
 
 
class ChatMessage(BaseModel):
    message: str
 
 
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
 
    def setup_routes(self):
        @self.app.get("/", response_class=FileResponse)
        async def read_root():
            if not HTML_FILE_PATH.exists():
                raise HTTPException(status_code=404, detail="Index file not found")
            return FileResponse(HTML_FILE_PATH)
 
        @self.app.post("/api/chat")
        async def chat_endpoint(request: ChatMessage):
            message = request.message
            logger.info(f"User: {message}")

            skill_reply = self.skill_manager.handle(message)
            if skill_reply is not None:
                logger.info(f"AXON (skill): {skill_reply}")
                return {"response": skill_reply}

            self.context.add_message("user", message)
            history = self.context.get_history()

            reply = self.hybrid_provider.generate(message, history=history)

            self.context.add_message("assistant", reply)
            logger.info(f"AXON: {reply}")

            return {"response": reply}
 
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