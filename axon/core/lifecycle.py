from axon.core.state import AppState
from axon.core.logger import logger
class Lifecycle:
    TRANSITIONS = {
        AppState.CREATED: [AppState.STARTING, AppState.ERROR],
        AppState.STARTING: [AppState.INITIALIZING, AppState.ERROR],
        AppState.INITIALIZING: [AppState.READY, AppState.ERROR],
        AppState.READY: [AppState.RUNNING, AppState.ERROR],
        AppState.RUNNING: [AppState.STOPPING, AppState.ERROR],
        AppState.STOPPING: [AppState.STOPPED, AppState.ERROR],
        AppState.ERROR: [AppState.STOPPING, AppState.STOPPED],
    }
    def __init__(self):
        self.state = AppState.CREATED
        
    def set_state(self, state: AppState):
        if state not in self.TRANSITIONS.get(self.state, []):
            raise ValueError(
                f"Invalid state transition: {self.state.value} -> {state.value}"
            )
            
        logger.info(f"State changed: {self.state.value} -> {state.value}")
        self.state = state