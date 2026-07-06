from pydantic import BaseModel
from typing import List, Optional

class TaxonomyNode(BaseModel):
    id: str
    name: str
    description: str
    parent_id: Optional[str] = None
    aliases: List[str] = []

class ClassificationRegistry(BaseModel):
    nodes: dict[str, TaxonomyNode] = {}

class ArtifactClassifier:
    def __init__(self, registry: ClassificationRegistry):
        self.registry = registry

    def classify(self, artifact_uri: str, taxonomy_id: str) -> None:
        pass
