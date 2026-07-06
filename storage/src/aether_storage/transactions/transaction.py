from typing import Protocol, runtime_checkable

@runtime_checkable
class StorageTransaction(Protocol):
    """Abstraction for storage transactions (ACID or non-ACID compensating)."""
    async def commit(self) -> None:
        ...
    async def rollback(self) -> None:
        ...
    async def compensate(self) -> None:
        ...
