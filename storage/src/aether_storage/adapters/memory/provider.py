from ...core.provider import StorageProvider
from ...core.handle import StorageHandle
from ...uri.resource_uri import ResourceURI
from typing import Any

class MemoryStorageProvider:
    """In-Memory implementation of StorageProvider for testing and ephemeral data."""
    async def open(self, uri: ResourceURI, mode: str = "r") -> StorageHandle:
        raise NotImplementedError
    async def close(self, handle: StorageHandle) -> None:
        pass
    async def exists(self, uri: ResourceURI) -> bool:
        return False
    async def resolve(self, uri: ResourceURI) -> ResourceURI:
        return uri
    async def stat(self, uri: ResourceURI) -> dict:
        return {}
    async def watch(self, uri: ResourceURI) -> Any:
        pass
    async def transaction(self, uri: ResourceURI) -> Any:
        pass
