from dataclasses import dataclass, field
from typing import Dict, Any, Optional
import uuid

@dataclass(frozen=True)
class RuntimeContext:
    user_id: str = "system"
    workspace_id: Optional[str] = None
    locale: str = "en-US"
    correlation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    permissions: tuple = field(default_factory=tuple)
    metadata: tuple = field(default_factory=tuple)  # Workaround for frozen Dict/List

    def copy_with(self, **kwargs):
        from dataclasses import replace
        return replace(self, **kwargs)
