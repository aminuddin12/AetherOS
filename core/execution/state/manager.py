from typing import Dict, Any
from core.execution.execution_session import ExecutionSession


class ExecutionStateManager:
    """
    State Manager khusus Execution Engine.
    Satu-satunya tempat mutable state boleh hidup.
    """

    def __init__(self):
        self._sessions: Dict[str, ExecutionSession] = {}
        self._execution_data: Dict[str, Any] = {}

    def store_session(self, session_id: str, session: ExecutionSession) -> None:
        self._sessions[session_id] = session

    def get_session(self, session_id: str) -> ExecutionSession | None:
        return self._sessions.get(session_id)

    def update_execution_data(self, session_id: str, data: Any) -> None:
        self._execution_data[session_id] = data

    def get_execution_data(self, session_id: str) -> Any:
        return self._execution_data.get(session_id)
