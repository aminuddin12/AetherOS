from typing import Any, Callable, Awaitable
from ..base import ContractProtocol

class EventDispatcherProtocol(ContractProtocol):
    """
    Abstraksi Event Bus (Routing & Dispatching) tanpa implementasi (mis: Redis).
    """
    async def publish(self, topic: str, event_data: Any) -> None:
        ...
        
    async def subscribe(self, topic: str, handler: Callable[[Any], Awaitable[None]]) -> None:
        ...
