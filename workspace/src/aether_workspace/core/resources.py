from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from enum import Enum
from datetime import datetime

class NodeType(Enum):
    FILE = "file"
    DIRECTORY = "directory"
    KNOWLEDGE = "knowledge"
    WORKFLOW = "workflow"
    SECRET = "secret"
    MODEL = "model"

class WorkspaceNode(BaseModel):
    id: str
    name: str
    type: NodeType
    path: str
    metadata: Dict[str, str] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class WorkspaceSnapshot(BaseModel):
    id: str
    workspace_id: str
    message: str
    author: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    nodes: List[WorkspaceNode] = Field(default_factory=list)
