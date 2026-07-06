from pydantic import BaseModel, Field
from typing import Dict, Any

class WorkspaceEnvironment(BaseModel):
    name: str = "Development"
    variables: Dict[str, str] = Field(default_factory=dict)
    secrets_ref: str = ""
    profiles: list = Field(default_factory=list)
    limits: Dict[str, Any] = Field(default_factory=dict)
