from typing import Dict, Any
from pydantic import Field
from ..base import Query
from ..common import ExecutionContext

class SystemQuery(Query):
    """
    Permintaan baca (Read request) asinkron dalam sistem (CQRS pattern).
    """
    target_component: str = Field(..., description="Target service or agent")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Query filters or params")
    context: ExecutionContext = Field(..., description="Execution context (Auth + Trace)")
