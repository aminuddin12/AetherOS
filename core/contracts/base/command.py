from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID, uuid4
from datetime import datetime, UTC


class Command(BaseModel):
    """
    Mewakili instruksi atau niat (intent) untuk mengubah state dalam sistem.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    command_id: UUID = Field(default_factory=uuid4, description="Unique identifier for the command")
    issued_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), description="When the command was issued"
    )
