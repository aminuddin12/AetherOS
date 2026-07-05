from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID, uuid4
from datetime import datetime, UTC

class Entity(BaseModel):
    """
    Base class untuk entitas domain yang memiliki identitas unik (ID).
    Dua entitas dikatakan sama jika memiliki ID yang sama, meskipun atribut lainnya berbeda.
    """
    model_config = ConfigDict(frozen=True, extra="forbid")

    id: UUID = Field(default_factory=uuid4, description="Global unique identifier for this entity")
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC), description="Creation timestamp")
    updated_at: datetime | None = Field(default=None, description="Last modification timestamp")
