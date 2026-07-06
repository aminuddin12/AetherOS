from typing import Dict, Any


class StateManager:
    """
    Satu-satunya komponen yang diperbolehkan memegang Mutable State global
    untuk Kernel, Worker, dan Task di luar AggregateRoot instances.
    """

    def __init__(self):
        self._kernel_state: Dict[str, Any] = {}
        self._worker_states: Dict[str, Any] = {}
        self._task_states: Dict[str, Any] = {}

    def get_kernel_state(self, key: str) -> Any:
        return self._kernel_state.get(key)

    def set_kernel_state(self, key: str, value: Any) -> None:
        self._kernel_state[key] = value

    def get_task_state(self, task_id: str) -> Any:
        return self._task_states.get(task_id)

    def set_task_state(self, task_id: str, state: Any) -> None:
        self._task_states[task_id] = state
