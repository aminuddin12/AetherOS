from pydantic import BaseModel
from typing import Dict, List
from ..relationships.models import ArtifactRelationship

class SemanticGraphNode(BaseModel):
    uri: str
    outbound_edges: List[ArtifactRelationship] = []
    inbound_edges: List[ArtifactRelationship] = []

class SemanticGraph(BaseModel):
    """
    A unified knowledge graph connecting diverse semantic artifacts.
    Company Brain primarily explores this graph.
    """
    nodes: Dict[str, SemanticGraphNode] = {}
