from typing import Any, Dict
from pydantic import Field
from ..base import DomainEvent


class TelemetryEvent(DomainEvent):
    """
    Event telemetri umum untuk pelacakan observability.
    """

    level: str = Field(default="info", description="Log level (info, warn, error)")
    message: str = Field(..., description="Telemetry message")
    attributes: Dict[str, Any] = Field(default_factory=dict, description="Structured log data")
