from pydantic import BaseModel
from typing import List

class ArtifactReference(BaseModel):
    """Reference to a specific semantic artifact."""
    uri: str

class LineageReference(BaseModel):
    """Reference for querying the semantic ancestry of an artifact."""
    artifact_uri: str

class ClassificationReference(BaseModel):
    """Reference to an artifact's semantic classification."""
    classification_id: str
