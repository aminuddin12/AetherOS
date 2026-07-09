from collections.abc import AsyncIterator
from dataclasses import dataclass, field
from typing import Any


@dataclass
class StorageHandle:
    uri: Any = None
    mode: str = "r"
    handle_id: str = ""
    raw_connection: Any = None
    metadata: dict[str, Any] = field(default_factory=dict)

    async def close(self) -> None:
        return None


@dataclass
class AsyncStreamHandle(StorageHandle):
    chunk_size: int = 1024 * 1024

    async def read_chunk(self, size: int = -1) -> bytes:
        return b""

    async def write_chunk(self, data: bytes) -> int:
        return len(data)

    async def stream(self, chunk_size: int = 1024 * 1024) -> AsyncIterator[bytes]:
        if False:
            yield b""
        return
