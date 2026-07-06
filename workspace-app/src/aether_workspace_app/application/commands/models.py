from pydantic import BaseModel
from ..context import ApplicationContext

class InitWorkspaceCommand(BaseModel):
    context: ApplicationContext
    workspace_name: str
    
class RegisterArtifactCommand(BaseModel):
    context: ApplicationContext
    classification_uri: str
    metadata: dict
