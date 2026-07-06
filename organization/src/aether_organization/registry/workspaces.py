from pydantic import BaseModel
from typing import Dict

class WorkspaceReference(BaseModel):
    uri: str
    name: str
    status: str

class OrganizationWorkspaceRegistry:
    """Manages WorkspaceReferences, not Workspace instances."""
    def __init__(self):
        self._workspaces: Dict[str, WorkspaceReference] = {}
        
    def register(self, workspace_ref: WorkspaceReference) -> None:
        self._workspaces[workspace_ref.uri] = workspace_ref
        
    def get(self, uri: str) -> WorkspaceReference:
        return self._workspaces.get(uri)
