from typing import Any
from ..base import ContractProtocol
from ..common import ExecutionContext

class RuntimeProtocol(ContractProtocol):
    """
    Abstraksi lingkungan eksekusi agen.
    (Tidak mengimplementasikan LangGraph atau framework tertentu).
    """
    async def initialize(self, context: ExecutionContext) -> None:
        ...
        
    async def execute_cycle(self, context: ExecutionContext, payload: Any) -> Any:
        ...
        
    async def shutdown(self) -> None:
        ...
