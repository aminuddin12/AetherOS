from typing import Any, Callable, Awaitable
from core.execution.spi import ExecutionMiddleware
from core.execution.internal import ExecutionValidationError


class ValidationMiddleware(ExecutionMiddleware):
    """Memvalidasi bahwa payload tidak kosong sebelum meneruskan."""

    async def invoke(self, context: Any, payload: Any, next_mw: Callable) -> Any:
        if payload is None:
            raise ExecutionValidationError("Payload cannot be None")
        return await next_mw(context, payload)
