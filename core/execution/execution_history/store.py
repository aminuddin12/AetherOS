from typing import List, Dict
from core.execution.execution_result import ExecutionResult

class ExecutionHistoryStore:
    """
    In-memory store untuk riwayat eksekusi.
    """
    def __init__(self, max_entries: int = 10000):
        self._history: Dict[str, ExecutionResult] = {}
        self._max = max_entries

    def record(self, session_id: str, result: ExecutionResult) -> None:
        if len(self._history) >= self._max:
            oldest_key = next(iter(self._history))
            del self._history[oldest_key]
        self._history[session_id] = result

    def get(self, session_id: str) -> ExecutionResult | None:
        return self._history.get(session_id)

    def list_recent(self, limit: int = 50) -> List[ExecutionResult]:
        return list(self._history.values())[-limit:]
