from enum import Enum

class ServiceState(Enum):
    UNINITIALIZED = "uninitialized"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    STOPPED = "stopped"
    FAILED = "failed"

class ServiceLifecycle:
    def __init__(self):
        self.state = ServiceState.UNINITIALIZED

    def transition_to(self, new_state: ServiceState):
        self.state = new_state
