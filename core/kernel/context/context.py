from typing import Dict, Any
from pydantic import BaseModel, Field


class KernelEnvironment(BaseModel):
    """Variabel statis dari OS Host"""

    os_name: str = Field(...)
    python_version: str = Field(...)
    variables: Dict[str, str] = Field(default_factory=dict)


class KernelContext(BaseModel):
    """Konteks makro tempat Kernel berjalan."""

    environment: KernelEnvironment
    global_metadata: Dict[str, Any] = Field(default_factory=dict)


class KernelRuntimeContext(BaseModel):
    """Konteks eksekusi sesaat yang diturunkan kepada Worker."""

    run_id: str
    tenant_id: str = "default"


class KernelExecutionContext(BaseModel):
    """Konteks spesifik untuk satu eksekusi pipeline."""

    correlation_id: str
    trace_id: str
    parent_id: str | None = None
