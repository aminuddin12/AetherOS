import time
from typing import Any, Callable
from core.execution.spi import ExecutionMiddleware
from core.execution.metrics import ExecutionMetricsCollector


class MetricsMiddleware(ExecutionMiddleware):
    """Merekam durasi dan status eksekusi."""

    def __init__(self, collector: ExecutionMetricsCollector):
        self._collector = collector

    async def invoke(self, context: Any, payload: Any, next_mw: Callable) -> Any:
        start = time.monotonic()
        try:
            result = await next_mw(context, payload)
            duration = (time.monotonic() - start) * 1000
            self._collector.record_execution("success", duration)
            return result
        except Exception as e:
            duration = (time.monotonic() - start) * 1000
            self._collector.record_execution("failure", duration)
            raise
