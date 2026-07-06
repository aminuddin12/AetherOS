from typing import Protocol, runtime_checkable, AsyncIterator, Union

@runtime_checkable
class StorageHandle(Protocol):
    """Base interface for all storage handles."""
    async def close(self) -> None:
        ...

@runtime_checkable
class AsyncStreamHandle(StorageHandle, Protocol):
    async def read_chunk(self, size: int = -1) -> bytes:
        ...
    async def write_chunk(self, data: bytes) -> int:
        ...
    async def stream(self, chunk_size: int = 1024 * 1024) -> AsyncIterator[bytes]:
        ...
