from pydantic import Field
from typing import List
from ..base import Entity

class KnowledgeFact(Entity):
    """
    Fakta teknis atau spesifikasi sistem yang diekstrak (Long-term Memory).
    """
    topic: str = Field(..., description="High level topic")
    content: str = Field(..., description="The factual knowledge content")
    tags: List[str] = Field(default_factory=list, description="Metadata tags for retrieval")
    confidence: float = Field(default=1.0, description="Truth probability")
