import logging
from pathlib import Path

logger = logging.getLogger("A.X.O.N")

def setup_logger():
    
    if logger.hasHandlers():
        return
    
    logger.handlers.clear()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S"
    )

    LOGS_DIR = Path("logs")
    LOGS_DIR.mkdir(exist_ok=True)

    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(
        LOGS_DIR / "axon.log",
        encoding="utf-8"
    )
    console_handler.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)

    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
