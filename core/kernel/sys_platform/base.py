from typing import Any, List, Dict
from pydantic import BaseModel

class RuntimeDescriptor(BaseModel):
    model_config = {"frozen": True}
    
    runtime_id: str
    display_name: str
    version: str
    api_version: str
    description: str
    author: str
    license: str
    tags: List[str]
    provides: List[str]
    requires: List[str]
    configuration_schema: Dict[str, Any]

class RuntimeState(BaseModel):
    lifecycle_state: str
    health_state: str
    started_at: float | None = None
    initialized_at: float | None = None
    last_error: str | None = None
    metrics: Dict[str, Any] = {}

class RuntimeContext(BaseModel):
    model_config = {"frozen": True}
    
    logger: Any
    configuration: Dict[str, Any]
    kernel: Any
    clock: Any
    metrics: Any
    event_bus: Any
    cancellation_token: Any
