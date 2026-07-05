from enum import StrEnum
from pydantic import Field
from ..base import AggregateRoot

class PRStatus(StrEnum):
    OPEN = "open"
    MERGED = "merged"
    CLOSED = "closed"
    DRAFT = "draft"

class PullRequest(AggregateRoot):
    """
    Permintaan penggabungan kode (Merge Request).
    """
    repository_id: str = Field(..., description="The repository")
    title: str = Field(..., description="PR Title")
    source_branch: str = Field(..., description="From branch")
    target_branch: str = Field(..., description="To branch")
    status: PRStatus = Field(default=PRStatus.OPEN)
