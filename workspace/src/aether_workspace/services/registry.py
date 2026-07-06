from typing import Dict, Any, List
from pydantic import BaseModel, Field

class WorkspaceRegistry(BaseModel):
    artifacts: Dict[str, Any] = Field(default_factory=dict)
    repositories: Dict[str, Any] = Field(default_factory=dict)
    workers: Dict[str, Any] = Field(default_factory=dict)
    knowledge_refs: Dict[str, Any] = Field(default_factory=dict)
    policies: Dict[str, Any] = Field(default_factory=dict)
    extensions: Dict[str, Any] = Field(default_factory=dict)

    def register_artifact(self, id: str, data: Any):
        self.artifacts[id] = data

    def register_worker(self, id: str, data: Any):
        self.workers[id] = data
