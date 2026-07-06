from typing import Any, List
from enum import StrEnum
from ..base import ContractProtocol


class MemoryScope(StrEnum):
    WORKSPACE = "workspace"
    PROJECT = "project"
    ORGANIZATION = "organization"
    GLOBAL = "global"


class MemoryProtocol(ContractProtocol):
    """
    Antarmuka mesin memori untuk menyimpan dan mencari wawasan (Retrieval).
    """

    async def store(self, scope: MemoryScope, context_id: str, payload: Any) -> str: ...

    async def retrieve(
        self, scope: MemoryScope, context_id: str, query: str, limit: int = 5
    ) -> List[Any]: ...
