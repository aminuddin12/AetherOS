from enum import Enum
from pydantic import BaseModel
from typing import List

class LifecycleState(str, Enum):
    DRAFT = "DRAFT"
    REVIEW = "REVIEW"
    APPROVED = "APPROVED"
    PUBLISHED = "PUBLISHED"
    DEPRECATED = "DEPRECATED"
    ARCHIVED = "ARCHIVED"
    DELETED = "DELETED"

class LifecycleTransition(BaseModel):
    from_state: LifecycleState
    to_state: LifecycleState
    reason: str

class ArtifactLifecycle(BaseModel):
    current_state: LifecycleState
    history: List[LifecycleTransition] = []
