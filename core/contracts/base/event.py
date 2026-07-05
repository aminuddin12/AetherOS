from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID, uuid4
from datetime import datetime, UTC

class DomainEvent(BaseModel):
    """
    Mewakili sesuatu yang telah terjadi di masa lalu di dalam domain.
    """
    model_config = ConfigDict(frozen=True, extra="forbid")

    event_id: UUID = Field(default_factory=uuid4, description="Unique identifier for the event")
    occurred_on: datetime = Field(default_factory=lambda: datetime.now(UTC), description="When the event occurred")
