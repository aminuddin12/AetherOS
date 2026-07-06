from typing import Protocol, runtime_checkable, Any
from ..uri.resource_uri import ResourceURI
from .handle import StorageHandle

@runtime_checkable
class StorageProvider(Protocol):
    """OS-like abstraction for storage providers."""
    
    async def open(self, uri: ResourceURI, mode: str = "r") -> StorageHandle:
        ...
        
    async def close(self, handle: StorageHandle) -> None:
        ...
        
    async def exists(self, uri: ResourceURI) -> bool:
        ...
        
    async def resolve(self, uri: ResourceURI) -> ResourceURI:
        ...
        
    async def stat(self, uri: ResourceURI) -> dict:
        ...
        
    async def watch(self, uri: ResourceURI) -> Any:
        ...
        
    async def transaction(self, uri: ResourceURI) -> Any:
        ...
