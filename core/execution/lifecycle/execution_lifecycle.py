from enum import StrEnum


class ExecutionState(StrEnum):
    CREATED = "created"
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"
    TIMED_OUT = "timed_out"


VALID_TRANSITIONS = {
    ExecutionState.CREATED: {ExecutionState.QUEUED, ExecutionState.CANCELLED},
    ExecutionState.QUEUED: {ExecutionState.RUNNING, ExecutionState.CANCELLED},
    ExecutionState.RUNNING: {
        ExecutionState.COMPLETED,
        ExecutionState.FAILED,
        ExecutionState.CANCELLED,
        ExecutionState.TIMED_OUT,
    },
    ExecutionState.COMPLETED: set(),
    ExecutionState.CANCELLED: set(),
    ExecutionState.FAILED: set(),
    ExecutionState.TIMED_OUT: set(),
}


class ExecutionLifecycle:
    """
    Mengelola dan memvalidasi transisi status eksekusi.
    """

    def __init__(self):
        self._state = ExecutionState.CREATED

    @property
    def state(self) -> ExecutionState:
        return self._state

    def transition_to(self, new_state: ExecutionState) -> bool:
        if new_state in VALID_TRANSITIONS.get(self._state, set()):
            self._state = new_state
            return True
        return False
