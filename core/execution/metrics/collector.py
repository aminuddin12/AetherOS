from typing import Dict
import time

class ExecutionMetricsCollector:
    """
    In-memory metrics collector untuk Execution Engine.
    """
    def __init__(self):
        self._counters: Dict[str, int] = {
            "execution_count": 0,
            "success_count": 0,
            "failure_count": 0,
            "timeout_count": 0,
            "retry_count": 0,
            "cancelled_count": 0,
        }
        self._durations: list[float] = []

    def record_execution(self, status: str, duration_ms: float = 0.0, retries: int = 0) -> None:
        self._counters["execution_count"] += 1
        self._counters["retry_count"] += retries
        self._durations.append(duration_ms)
        if status == "success":
            self._counters["success_count"] += 1
        elif status == "failure":
            self._counters["failure_count"] += 1
        elif status == "timeout":
            self._counters["timeout_count"] += 1
        elif status == "cancelled":
            self._counters["cancelled_count"] += 1

    def get_average_duration(self) -> float:
        if not self._durations:
            return 0.0
        return sum(self._durations) / len(self._durations)

    def snapshot(self) -> Dict[str, int | float]:
        result = dict(self._counters)
        result["average_duration_ms"] = self.get_average_duration()
        return result
