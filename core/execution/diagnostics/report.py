from typing import Dict, Any
from core.execution.executor_pool import ExecutorPool
from core.execution.metrics import ExecutionMetricsCollector


class ExecutionDiagnostics:
    """
    Menghasilkan laporan diagnostik Execution Engine.
    """

    def __init__(self, pool: ExecutorPool, metrics: ExecutionMetricsCollector):
        self._pool = pool
        self._metrics = metrics

    def report(self) -> Dict[str, Any]:
        return {
            "available_executors": self._pool.list_available(),
            "metrics": self._metrics.snapshot(),
        }
