from enum import Enum

class AppState(Enum):
    CREATED = "created"
    STARTING = "starting"
    INITIALIZING = "initializing"
    READY = "ready"
    RUNNING = "running"
    STOPPING = "stopping"
    STOPPED = "stopped"
    ERROR = "error"
    