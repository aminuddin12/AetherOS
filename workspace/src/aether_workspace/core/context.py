from dataclasses import dataclass, field
from typing import Dict, Optional

@dataclass(frozen=True)
class WorkspaceContext:
    workspace_id: str
    organization_id: str
    project_id: Optional[str] = None
    user_id: str = "system"
    worker_id: Optional[str] = None
    locale: str = "en-US"
    timezone: str = "UTC"
    execution_id: Optional[str] = None
    trace_id: Optional[str] = None
