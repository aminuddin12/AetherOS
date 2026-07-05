from pydantic import Field
from ..base import Entity

class Repository(Entity):
    """
    Representasi dari VCS repo (Git).
    """
    workspace_id: str = Field(..., description="Workspace owning the repo")
    name: str = Field(..., description="Repo name")
    remote_url: str = Field(..., description="Git remote URL")
