from pydantic import BaseModel

class WorkspaceInitialized(BaseModel):
    workspace_uri: str
    timestamp: str
    
class ArtifactRegistered(BaseModel):
    artifact_uri: str
    workspace_uri: str
    timestamp: str

class StorageMounted(BaseModel):
    workspace_uri: str
    storage_uri: str
    timestamp: str
