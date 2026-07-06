from enum import StrEnum
from typing import Any, Dict
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime, UTC

class ExecutionStatus(StrEnum):
    SUCCESS = "success"
    FAILURE = "failure"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"
    RETRY_EXHAUSTED = "retry_exhausted"

class ExecutionResult(BaseModel):
    """
    Hasil eksekusi. Immutable setelah dibuat.
    """
    model_config = ConfigDict(frozen=True)

    status: ExecutionStatus = Field(...)
    output: Any = Field(default=None)
    error: str | None = Field(default=None)
    duration_ms: float = Field(default=0.0)
    retry_count: int = Field(default=0)
    completed_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    metadata: Dict[str, Any] = Field(default_factory=dict)
