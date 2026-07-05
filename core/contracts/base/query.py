from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID, uuid4
from datetime import datetime, UTC

class Query(BaseModel):
    """
    Mewakili permintaan untuk mengambil data tanpa memodifikasi state (side-effect free).
    """
    model_config = ConfigDict(frozen=True, extra="forbid")

    query_id: UUID = Field(default_factory=uuid4, description="Unique identifier for the query")
    issued_at: datetime = Field(default_factory=lambda: datetime.now(UTC), description="When the query was issued")
