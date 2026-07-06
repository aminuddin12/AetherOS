import asyncio
from typing import Any, Callable, Awaitable
from core.execution.spi import TimeoutPolicy
from core.execution.internal import ExecutionTimeoutError

class TimeoutHandler:
    """
    Menjalankan callable dengan batas waktu.
    """
    def __init__(self, policy: TimeoutPolicy):
        self._policy = policy

    async def execute_with_timeout(self, fn: Callable[..., Awaitable[Any]], *args: Any, **kwargs: Any) -> Any:
        try:
            return await asyncio.wait_for(
                fn(*args, **kwargs),
                timeout=self._policy.execution_timeout_seconds
            )
        except asyncio.TimeoutError:
            raise ExecutionTimeoutError(
                f"Execution exceeded {self._policy.execution_timeout_seconds}s timeout"
            )
