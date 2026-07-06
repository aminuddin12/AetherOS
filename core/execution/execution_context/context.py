from typing import Dict, Any
from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID, uuid4

class ExecutionContext(BaseModel):
    """
    Context immutable yang diturunkan ke Executor.
    Berisi semua informasi yang dibutuhkan executor untuk menjalankan tugas.
    """
    model_config = ConfigDict(frozen=True)

    context_id: UUID = Field(default_factory=uuid4)
    correlation_id: str = Field(...)
    trace_id: str = Field(...)
    parent_context_id: UUID | None = Field(default=None)
    tenant_id: str = Field(default="default")
    namespace: str = Field(default="default")
    metadata: Dict[str, Any] = Field(default_factory=dict)
