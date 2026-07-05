from typing import Callable, List, Dict, Type
import asyncio
from core.contracts.base import DomainEvent
from .policy import SupervisorPolicy

class EventBus:
    """
    Pure Pub/Sub Event Dispatcher.
    Tidak menyimpan antrian atau retry logic.
    Menyerahkan penanganan error kepada Supervisor Policy.
    """
    def __init__(self, policy: SupervisorPolicy = SupervisorPolicy.TELEMETRY):
        self._subscribers: Dict[Type[DomainEvent], List[Callable]] = {}
        self._policy = policy

    def subscribe(self, event_type: Type[DomainEvent], handler: Callable) -> None:
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)

    async def publish(self, event: DomainEvent) -> None:
        event_type = type(event)
        handlers = self._subscribers.get(event_type, [])
        for handler in handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(event)
                else:
                    handler(event)
            except Exception as e:
                self._handle_error(e, event)

    def _handle_error(self, error: Exception, event: DomainEvent) -> None:
        if self._policy == SupervisorPolicy.RAISE:
            raise error
        elif self._policy == SupervisorPolicy.IGNORE:
            pass
        # Other policies handled appropriately (e.g. sent to DLQ or Telemetry)
