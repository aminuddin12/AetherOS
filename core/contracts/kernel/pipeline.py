from typing import Any, List
from ..base import ContractProtocol
from ..common import ExecutionContext


class ExecutionPipelineProtocol(ContractProtocol):
    """
    Kontrak untuk memvalidasi dan memproses instruksi
    melewati beberapa tahap middleware sebelum dieksekusi.
    """

    async def process(self, context: ExecutionContext, steps: List[Any]) -> Any: ...
