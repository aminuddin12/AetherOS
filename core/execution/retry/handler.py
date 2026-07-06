import asyncio
from typing import Any, Callable, Awaitable
from core.execution.spi import RetryPolicy
from core.execution.internal import ExecutionRetryExhaustedError

class RetryHandler:
    """
    Menjalankan callable dengan retry berdasarkan policy.
    """
    def __init__(self, policy: RetryPolicy):
        self._policy = policy

    async def execute_with_retry(self, fn: Callable[..., Awaitable[Any]], *args: Any, **kwargs: Any) -> Any:
        last_error: Exception | None = None
        for attempt in range(self._policy.max_retries + 1):
            try:
                return await fn(*args, **kwargs)
            except Exception as e:
                last_error = e
                if not self._policy.should_retry(attempt, e):
                    break
                delay = self._policy.get_delay(attempt)
                await asyncio.sleep(delay)
        raise ExecutionRetryExhaustedError(f"All {self._policy.max_retries} retries exhausted: {last_error}")
