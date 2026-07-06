from pydantic import BaseModel
from typing import Optional

class ApplicationContext(BaseModel):
    """
    Context that wraps Organization, Workspace, and Session.
    Prepares M3.4 for transition to M3.5.
    """
    organization_id: str
    workspace_id: str
    session_id: str
    user_id: str
    correlation_id: str
