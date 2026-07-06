from typing import Protocol, runtime_checkable, List
from ..core.domain import Artifact
from ..references.models import ArtifactReference

@runtime_checkable
class ArtifactBackend(Protocol):
    """Abstract interface for the Artifact Database/Registry."""
    
    async def register(self, artifact: Artifact) -> ArtifactReference:
        ...
        
    async def resolve(self, reference: ArtifactReference) -> Artifact:
        ...
        
    async def query(self, classification_id: str) -> List[Artifact]:
        ...
        
    async def update_lifecycle(self, reference: ArtifactReference, new_state: str) -> None:
        ...
