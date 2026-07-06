from enum import StrEnum
from typing import List
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime, UTC


class SessionStatus(StrEnum):
    CREATED = "created"
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"
    TIMED_OUT = "timed_out"


class ExecutionSession(BaseModel):
    """
    Session runtime yang membungkus satu unit eksekusi.
    """

    session_id: UUID = Field(default_factory=uuid4)
    parent_session_id: UUID | None = Field(default=None)
    child_session_ids: List[UUID] = Field(default_factory=list)
    status: SessionStatus = Field(default=SessionStatus.CREATED)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    started_at: datetime | None = Field(default=None)
    completed_at: datetime | None = Field(default=None)
    correlation_id: str = Field(default="")
