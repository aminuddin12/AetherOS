from pydantic import Field
from ..base import AggregateRoot

class Project(AggregateRoot):
    """
    Unit inisiatif bisnis di dalam organisasi (membawahi Workspace).
    """
    organization_id: str = Field(..., description="Owning organization")
    name: str = Field(..., description="Project name")
    description: str = Field(..., description="Project goals and scope")
