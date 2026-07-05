from pydantic import Field
from typing import Dict, Any
from ..base import ValueObject
from ..identity import AuthenticationContext
from .trace import TraceContext

class ExecutionContext(ValueObject):
    """
    Pembungkus state runtime untuk eksekusi yang sedang berjalan.
    Menyediakan info tentang 'Siapa', 'Kapan', dan 'Pelacakan apa' yang memicu aksi.
    """
    auth: AuthenticationContext = Field(..., description="Current authentication details")
    trace: TraceContext = Field(..., description="Observability trace details")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional contextual metadata")
