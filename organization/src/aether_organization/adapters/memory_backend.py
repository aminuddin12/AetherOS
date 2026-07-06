from typing import Dict
from ..protocols.backend import OrganizationBackend
from ..directory.membership import OrganizationMembership
from ..registry.workspaces import WorkspaceReference

class MemoryOrganizationBackend:
    """In-Memory implementation of the Organization Backend (M3.5 Stub)."""
    
    def __init__(self):
        self.members: Dict[str, OrganizationMembership] = {}
        self.workspaces: Dict[str, WorkspaceReference] = {}
        
    async def save_member(self, member: OrganizationMembership) -> None:
        self.members[member.member_id] = member
        
    async def get_member(self, member_id: str) -> OrganizationMembership:
        return self.members.get(member_id)
        
    async def register_workspace_ref(self, ref: WorkspaceReference) -> None:
        self.workspaces[ref.uri] = ref
