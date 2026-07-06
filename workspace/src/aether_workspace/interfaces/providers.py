from typing import Protocol, runtime_checkable
from datetime import datetime

@runtime_checkable
class ClockProvider(Protocol):
    def utcnow(self) -> datetime:
        ...

@runtime_checkable
class EventStoreProvider(Protocol):
    async def save_event(self, event_type: str, payload: dict) -> None:
        ...

@runtime_checkable
class IdentityProvider(Protocol):
    async def get_current_user_id(self) -> str:
        ...

@runtime_checkable
class PolicyProvider(Protocol):
    async def evaluate_policy(self, context: dict, action: str) -> bool:
        ...

@runtime_checkable
class WorkspaceProvider(Protocol):
    async def load_workspace(self, workspace_id: str) -> dict:
        ...

class MemoryClockProvider:
    def utcnow(self) -> datetime:
        return datetime.utcnow()
