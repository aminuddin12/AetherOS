from enum import StrEnum
from pydantic import Field
from ..base import Entity


class IssuePriority(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    BLOCKER = "blocker"


class Issue(Entity):
    """
    Representasi dari masalah teknis atau bug report (yang akan melahirkan Task).
    """

    title: str = Field(..., description="Issue title")
    body: str = Field(..., description="Issue details/reproduction steps")
    priority: IssuePriority = Field(default=IssuePriority.MEDIUM)
