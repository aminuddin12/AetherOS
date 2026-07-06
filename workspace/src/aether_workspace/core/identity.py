from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

class WorkspaceMetadata(BaseModel):
    labels: Dict[str, str] = Field(default_factory=dict)
    annotations: Dict[str, str] = Field(default_factory=dict)
    tags: List[str] = Field(default_factory=list)
    classification: str = "internal"
    environment: str = "development"
    region: str = "global"

class WorkspaceDescriptor(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    owner: str = "system"
    version: str = "1.0.0"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: WorkspaceMetadata = Field(default_factory=WorkspaceMetadata)

class WorkspaceCapabilities(BaseModel):
    supports_git: bool = False
    supports_ai: bool = False
    supports_plugins: bool = False
    supports_distribution: bool = False
    supports_cache: bool = False

class WorkspacePolicies(BaseModel):
    read_access: str = "private"
    write_access: str = "owner"
    execution_allowed: bool = True
    knowledge_sharing: bool = False
    security_level: str = "standard"
    retention_days: int = 365
    audit_enabled: bool = True

class WorkspaceManifest(BaseModel):
    policies: WorkspacePolicies = Field(default_factory=WorkspacePolicies)
    capabilities: WorkspaceCapabilities = Field(default_factory=WorkspaceCapabilities)
    extensions: Dict[str, Any] = Field(default_factory=dict)
    permissions: Dict[str, List[str]] = Field(default_factory=dict)
