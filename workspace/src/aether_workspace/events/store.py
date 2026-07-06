from typing import Dict, Any, List
from pydantic import BaseModel, Field

class WorkspaceEvent(BaseModel):
    id: str
    type: str
    payload: Dict[str, Any]
    timestamp: str

class EventStore:
    def __init__(self):
        self.events: List[WorkspaceEvent] = []
        
    def append(self, event: WorkspaceEvent):
        self.events.append(event)

class EventDispatcher:
    pass

class EventReplay:
    pass
