from ..protocols.backend import ArtifactBackend
from ..core.domain import Artifact
from ..references.models import ArtifactReference
from typing import List, Dict

class MemoryArtifactBackend:
    """In-Memory implementation of the Artifact Registry."""
    
    def __init__(self):
        self.artifacts: Dict[str, Artifact] = {}
        
    async def register(self, artifact: Artifact) -> ArtifactReference:
        self.artifacts[artifact.id] = artifact
        return ArtifactReference(uri=f"artifact://{artifact.classification_uri}/{artifact.id}")
        
    async def resolve(self, reference: ArtifactReference) -> Artifact:
        # Simplistic resolution by extracting id
        artifact_id = reference.uri.split('/')[-1]
        return self.artifacts[artifact_id]
        
    async def query(self, classification_id: str) -> List[Artifact]:
        return [a for a in self.artifacts.values() if a.classification_uri == classification_id]
        
    async def update_lifecycle(self, reference: ArtifactReference, new_state: str) -> None:
        artifact_id = reference.uri.split('/')[-1]
        if artifact_id in self.artifacts:
            self.artifacts[artifact_id].lifecycle_state = new_state
