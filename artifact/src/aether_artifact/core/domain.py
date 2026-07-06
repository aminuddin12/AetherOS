from pydantic import BaseModel
from typing import Any, Dict

class MetadataSchemaReference(BaseModel):
    """Reference to a schema defining the structure of metadata."""
    schema_uri: str
    version: str

class MetadataInstance(BaseModel):
    """Concrete metadata payload adhering to a schema."""
    schema_ref: MetadataSchemaReference
    payload: Dict[str, Any]

class Artifact(BaseModel):
    """
    Semantic Resource representing a discrete node of knowledge.
    This does NOT hold the blob. It points to a Storage URI.
    """
    id: str
    name: str
    storage_uri: str  # e.g., storage://workspace/backend/blob-id
    classification_uri: str
    metadata: MetadataInstance
    lifecycle_state: str
