from pydantic import BaseModel
from typing import Dict, Any

class PlatformEvent(BaseModel):
    model_config = {"frozen": True}
    
    runtime_id: str
    timestamp: float

class RuntimeLifecycleChangedEvent(PlatformEvent):
    old_state: str
    new_state: str

class RuntimeHealthChangedEvent(PlatformEvent):
    old_health: str
    new_health: str
    trigger_reason: str | None = None
