from typing import Protocol, runtime_checkable
from ..directory.membership import OrganizationMembership
from ..registry.workspaces import WorkspaceReference

@runtime_checkable
class OrganizationBackend(Protocol):
    """Abstract interface for the Organization Database."""
    
    async def save_member(self, member: OrganizationMembership) -> None:
        ...
        
    async def get_member(self, member_id: str) -> OrganizationMembership:
        ...
        
    async def register_workspace_ref(self, ref: WorkspaceReference) -> None:
        ...
