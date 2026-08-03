from axon.core.state import AppState
from axon.core.logger import logger, setup_logger
from axon.core.config import Config

class Application:
    """
    Main application class.

    Coordinates all A.X.O.N. modules.
    """

    VERSION = "0.1.0"

    def __init__(self):
        self.running = False
        self.state = AppState.CREATED
        self.config = Config()
        
    def run(self):
        self.running = True
        
        setup_logger()
        self.config.load()
        logger.info("=" * 50)
        logger.info(f"A.X.O.N. v{self.VERSION}")
        logger.info("=" * 50)
        logger.info("Initializing Core...")
        logger.info("Loading Configuration...")
        logger.info("Starting Services...")
        logger.info("✔ Core initialized.")
        logger.info("✔ Ready.")
        