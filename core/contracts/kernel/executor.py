from typing import Any
from ..base import ContractProtocol
from ..common import ExecutionContext

class SandboxExecutorProtocol(ContractProtocol):
    """
    Antarmuka untuk Sandbox Tool Execution (mis: abstraksi atas OpenHands/Docker).
    """
    async def execute_command(self, context: ExecutionContext, command: str) -> str:
        ...
        
    async def execute_code(self, context: ExecutionContext, language: str, code: str) -> Any:
        ...
