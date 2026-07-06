from pydantic import BaseModel
from typing import List

class Capabilities(BaseModel):
    is_searchable: bool = False
    is_executable: bool = False
    is_renderable: bool = False
    is_embeddable: bool = False
    is_versioned: bool = False
    is_editable: bool = False
    is_indexable: bool = False

class CapabilityRegistry:
    def get_capabilities(self, artifact_uri: str) -> Capabilities:
        return Capabilities()
