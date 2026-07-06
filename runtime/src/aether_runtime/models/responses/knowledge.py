from pydantic import BaseModel, Field
from typing import Dict, List, Any


class KnowledgeDocument(BaseModel):
    uri: str = Field(..., description="Canonical resource URI for the knowledge node")
    title: str = Field(..., description="Short title describing the knowledge item")
    summary: str = Field(..., description="Brief summary of the indexed knowledge content")
    tags: List[str] = Field(default_factory=list, description="Semantic tags for retrieval")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata associated with the document")


class KnowledgeResource(BaseModel):
    """Aggregated runtime resource information for Company Brain indexing."""
    uri: str = Field(..., description="Original resource URI")
    identifier: str = Field(..., description="Resolved resource identifier")
    artifact_info: Dict[str, Any] = Field(default_factory=dict, description="Artifact resolution data")
    repository_graph: Dict[str, Any] = Field(default_factory=dict, description="Repository graph structure")
    workspace_context: Dict[str, Any] = Field(default_factory=dict, description="Workspace metadata")
    storage_metadata: Dict[str, Any] = Field(default_factory=dict, description="Storage resolution data")
    organization_info: Dict[str, Any] = Field(default_factory=dict, description="Ownership and identity information")
    title: str = Field(..., description="Generated title for the resource")
    summary: str = Field(..., description="Generated summary of the resource")


class KnowledgeQueryResult(BaseModel):
    query: str = Field(..., description="Original query string")
    results: List[KnowledgeDocument] = Field(default_factory=list, description="Matching knowledge documents")
    total: int = Field(..., description="Total matching documents")
    scored: Dict[str, float] = Field(default_factory=dict, description="Match scores keyed by document URI")


class KnowledgeGraphSummary(BaseModel):
    node_count: int = Field(..., description="Number of indexed knowledge nodes")
    edge_count: int = Field(..., description="Number of inferred relationships")
    known_domains: List[str] = Field(default_factory=list, description="Resource namespaces discovered during indexing")
