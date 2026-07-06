from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Commit(BaseModel):
    """Immutable snapshot of the tree state."""
    id: str
    author: str
    message: str
    timestamp: datetime
    parents: List[str] = []
    tree_uri: Optional[str] = None  # URI to storage snapshot

class Branch(BaseModel):
    """Pointer to a specific revision."""
    name: str
    target_revision_id: str
    is_default: bool = False
    
class Revision(BaseModel):
    """Generic wrapper for an identified point in history."""
    id: str
    commit_id: str
    
class Merge(BaseModel):
    """Represents a merge action between two branches/revisions."""
    source_revision_id: str
    target_revision_id: str
    result_commit_id: str
    
class Diff(BaseModel):
    """Difference between two revisions."""
    base_revision_id: str
    target_revision_id: str
    changes: List[dict]
    
class History(BaseModel):
    """Ordered history of a branch or revision."""
    revisions: List[str]
