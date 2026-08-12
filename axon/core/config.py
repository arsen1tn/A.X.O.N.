import json
from pathlib import Path
from axon.core.logger import logger



class Config:
    """
    Configuration manager for A.X.O.N.
    """

    def __init__(self):
        self.config = {}
    
    def load(self):
        config_path = Path("config/config.json")
        
        try:
            with config_path.open("r", encoding="utf-8") as file:
                self.config = json.load(file)
            return True
        
        except FileNotFoundError:
            logger.error("Configuration file not found.")
            return False
    
        except json.JSONDecodeError:
            logger.error("Configuration file contains invalid JSON.")
            return False
        
    def get(self, key, default=None):
        keys = key.split(".")
        value = self.config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value
    