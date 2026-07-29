import logging
from pathlib import Path

logger = logging.getLogger("A.X.O.N")
logger.setLevel(logging.INFO)

LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)

console_handler = logging.StreamHandler()
file_handler = logging.FileHandler(
    LOGS_DIR / "axon.log",
    encoding="utf-8"
)
file_handler.setLevel(logging.INFO)
console_handler.setLevel(logging.INFO)
logger.addHandler(console_handler)
logger.addHandler(file_handler)
logger.info("Logger initialized successfully.")