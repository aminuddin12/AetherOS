from pydantic import BaseModel

class WorkspaceInitializationResult(BaseModel):
    workspace_uri: str
    storage_uri: str
    repository_uri: str
    success: bool

class ArtifactRegistrationResult(BaseModel):
    artifact_uri: str
    lineage_graph_updated: bool
    success: bool
