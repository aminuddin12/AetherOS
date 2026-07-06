from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class WorkspaceSession(BaseModel):
    id: str
    workspace_id: str
    user_id: str
    runtime_info: str
    opened_at: datetime
    expires_at: Optional[datetime] = None
    capabilities: list = []

class SessionManager:
    def current(self) -> Optional[WorkspaceSession]:
        return None
