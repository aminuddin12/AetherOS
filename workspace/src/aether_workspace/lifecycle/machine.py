from enum import Enum
from pydantic import BaseModel

class WorkspaceState(Enum):
    UNINITIALIZED = "Uninitialized"
    INITIALIZING = "Initializing"
    READY = "Ready"
    LOCKED = "Locked"
    BUSY = "Busy"
    SUSPENDED = "Suspended"
    MAINTENANCE = "Maintenance"
    SNAPSHOTTING = "Snapshotting"
    ARCHIVING = "Archiving"
    ARCHIVED = "Archived"
    DELETED = "Deleted"

class StateMachine:
    def __init__(self):
        self.state = WorkspaceState.UNINITIALIZED
    
    def transition_to(self, new_state: WorkspaceState):
        # Basic validation can be added here
        self.state = new_state
