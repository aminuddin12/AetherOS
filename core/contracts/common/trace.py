from pydantic import Field
from uuid import UUID, uuid4
from datetime import datetime, UTC
from ..base import ValueObject


class TraceSpan(ValueObject):
    """
    Unit dasar dalam OpenTelemetry-style tracing.
    """

    span_id: UUID = Field(default_factory=uuid4, description="Unique ID for this span")
    parent_span_id: UUID | None = Field(default=None, description="ID of the parent span")
    name: str = Field(..., description="Name of the operation")
    started_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), description="Span start time"
    )
    ended_at: datetime | None = Field(default=None, description="Span end time")


class TraceContext(ValueObject):
    """
    Konteks pelacakan eksekusi untuk observability.
    """

    trace_id: UUID = Field(default_factory=uuid4, description="Global trace identifier")
    current_span: TraceSpan | None = Field(default=None, description="Active span in this context")
