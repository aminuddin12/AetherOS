from pydantic import Field
from uuid import UUID, uuid4
from datetime import datetime, UTC
from .contract import BaseContract

class Entity(BaseContract):
    """
    Base class untuk entitas domain yang memiliki identitas unik (ID) dan lifecycle.
    Mewarisi BaseContract sehingga memiliki full metadata & versioning.
    """
    id: UUID = Field(default_factory=uuid4, description="Global unique identifier for this entity")
    namespace: str = Field(default="default", description="Namespace isolating this entity")
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC), description="Creation timestamp")
    updated_at: datetime | None = Field(default=None, description="Last modification timestamp")
