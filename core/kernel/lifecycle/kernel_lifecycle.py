from enum import Enum


class KernelState(Enum):
    PRE_BOOTSTRAP = "pre_bootstrap"
    BOOTSTRAPPING = "bootstrapping"
    POST_BOOTSTRAP = "post_bootstrap"
    READY = "ready"
    RUNNING = "running"
    SHUTTING_DOWN = "shutting_down"
    TERMINATED = "terminated"


class KernelLifecycle:
    def __init__(self):
        self.state = KernelState.PRE_BOOTSTRAP

    def transition_to(self, new_state: KernelState):
        self.state = new_state
