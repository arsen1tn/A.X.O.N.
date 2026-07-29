from axon.core.state import AppState
from axon.core.logger import logger

class Application:
    """
    Main application class.

    Coordinates all A.X.O.N. modules.
    """

    VERSION = "0.1.0"

    def __init__(self):
        self.running = False
        self.state = AppState.CREATED
        
    def run(self):
        self.running = True

        print("=" * 50)
        print(f"A.X.O.N. v{self.VERSION}")
        print("=" * 50)
        logger.info("Initializing Core...")
        print("Loading Configuration...")
        print("Starting Services...")
        print()
        print("✔ Core initialized.")
        print("✔ Ready.")
        