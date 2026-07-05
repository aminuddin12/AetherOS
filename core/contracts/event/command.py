from typing import Dict, Any
from pydantic import Field
from ..base import Command
from ..common import ExecutionContext

class SystemCommand(Command):
    """
    Intensi untuk mengeksekusi operasi asinkron dalam sistem (CQRS pattern).
    """
    target_component: str = Field(..., description="Target service or agent")
    payload: Dict[str, Any] = Field(default_factory=dict, description="Command arguments")
    context: ExecutionContext = Field(..., description="Execution context (Auth + Trace)")
