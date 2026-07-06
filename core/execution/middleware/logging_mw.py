import logging
from typing import Any, Callable
from core.execution.spi import ExecutionMiddleware

logger = logging.getLogger("aether.execution")


class LoggingMiddleware(ExecutionMiddleware):
    """Logging middleware untuk observability."""

    async def invoke(self, context: Any, payload: Any, next_mw: Callable) -> Any:
        logger.info("Execution started")
        try:
            result = await next_mw(context, payload)
            logger.info("Execution completed successfully")
            return result
        except Exception as e:
            logger.error(f"Execution failed: {e}")
            raise
