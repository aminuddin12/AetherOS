from typing import Dict, Any
from pydantic import Field
from ..base import DomainEvent
from ..common import TraceContext

class SystemEvent(DomainEvent):
    """
    Event lintas komponen yang disebarkan via Event Bus.
    """
    topic: str = Field(..., description="Routing topic for the event")
    payload: Dict[str, Any] = Field(default_factory=dict, description="Event data")
    trace: TraceContext = Field(..., description="Trace context for observability")
