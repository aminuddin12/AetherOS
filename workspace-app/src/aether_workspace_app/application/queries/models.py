from pydantic import BaseModel
from ..context import ApplicationContext

class InspectHistoryQuery(BaseModel):
    context: ApplicationContext
    artifact_uri: str
    
class ListArtifactsQuery(BaseModel):
    context: ApplicationContext
    classification: str
