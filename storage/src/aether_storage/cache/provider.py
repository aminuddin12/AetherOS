from typing import Protocol, runtime_checkable, Any
from ..uri.resource_uri import ResourceURI

@runtime_checkable
class CacheProvider(Protocol):
    """Provider for caching resources to minimize latency."""
    async def get(self, uri: ResourceURI) -> Any:
        ...
    async def put(self, uri: ResourceURI, data: Any, ttl: int = 3600) -> None:
        ...
    async def invalidate(self, uri: ResourceURI) -> None:
        ...
