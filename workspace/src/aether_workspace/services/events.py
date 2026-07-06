from enum import Enum
from typing import Callable, Dict, List

class WorkspaceEventType(Enum):
    CREATED = "WorkspaceCreated"
    OPENED = "WorkspaceOpened"
    CLOSED = "WorkspaceClosed"
    LOCKED = "WorkspaceLocked"
    UNLOCKED = "WorkspaceUnlocked"
    ARCHIVED = "WorkspaceArchived"
    INITIALIZED = "WorkspaceInitialized"
    DISPOSED = "WorkspaceDisposed"

class WorkspaceEventBus:
    def __init__(self):
        self.listeners: Dict[str, List[Callable]] = {}

    def subscribe(self, event_type: WorkspaceEventType, callback: Callable):
        if event_type.value not in self.listeners:
            self.listeners[event_type.value] = []
        self.listeners[event_type.value].append(callback)

    async def emit(self, event_type: WorkspaceEventType, **kwargs):
        for callback in self.listeners.get(event_type.value, []):
            await callback(**kwargs)

event_bus = WorkspaceEventBus()
