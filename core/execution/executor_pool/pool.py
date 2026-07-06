from typing import Dict, List, Any
from core.execution.spi import Executor
from core.execution.internal import ExecutorNotFoundError, ExecutorAllocationError


class ExecutorPool:
    """
    Pool pengelola Executor instances.
    """

    def __init__(self):
        self._executors: Dict[str, Executor] = {}
        self._allocated: Dict[str, str] = {}

    def register(self, executor_id: str, executor: Executor) -> None:
        self._executors[executor_id] = executor

    def unregister(self, executor_id: str) -> None:
        self._executors.pop(executor_id, None)
        self._allocated = {k: v for k, v in self._allocated.items() if v != executor_id}

    def lookup(self, executor_id: str) -> Executor:
        executor = self._executors.get(executor_id)
        if not executor:
            raise ExecutorNotFoundError(f"Executor '{executor_id}' not found in pool")
        return executor

    def allocate(self, session_id: str, executor_id: str | None = None) -> Executor:
        if executor_id:
            executor = self.lookup(executor_id)
            self._allocated[session_id] = executor_id
            return executor
        for eid, ex in self._executors.items():
            if eid not in self._allocated.values():
                self._allocated[session_id] = eid
                return ex
        raise ExecutorAllocationError("No available executors in pool")

    def release(self, session_id: str) -> None:
        self._allocated.pop(session_id, None)

    def list_available(self) -> List[str]:
        allocated_ids = set(self._allocated.values())
        return [eid for eid in self._executors if eid not in allocated_ids]
