from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Dict

class WorkspaceHealth(Enum):
    HEALTHY = "Healthy"
    BUSY = "Busy"
    LOCKED = "Locked"
    CORRUPTED = "Corrupted"
    ARCHIVED = "Archived"
    RECOVERING = "Recovering"

class WorkspaceSessionState(Enum):
    OPEN = "Open"
    IDLE = "Idle"
    BUSY = "Busy"
    CLOSING = "Closing"
    CLOSED = "Closed"

@dataclass(frozen=True)
class WorkspaceContext:
    workspace_id: str
    organization: str = "default-org"
    division: str = "general"
    locale: str = "en-US"
    timezone: str = "UTC"
    variables: Dict[str, str] = field(default_factory=dict)
    secrets_ref: Optional[str] = None
    policy_ref: Optional[str] = None
    knowledge_ref: Optional[str] = None

class WorkspaceSession:
    def __init__(self, context: WorkspaceContext):
        self._context = context
        self.state = WorkspaceSessionState.CLOSED
        self.health = WorkspaceHealth.HEALTHY

    @property
    def context(self) -> WorkspaceContext:
        return self._context

    def open(self):
        self.state = WorkspaceSessionState.OPEN

    def close(self):
        self.state = WorkspaceSessionState.CLOSED
