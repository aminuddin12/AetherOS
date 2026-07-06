from pydantic import Field
from ..base import ValueObject


class ResourceUsage(ValueObject):
    """
    Konsumsi sumber daya non-LLM (CPU, Memori, Durasi Sandbox).
    """

    execution_time_ms: int = Field(
        default=0, description="Total execution duration in milliseconds"
    )
    peak_memory_mb: float = Field(default=0.0, description="Peak memory consumption in MB")
