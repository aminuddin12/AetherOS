from pydantic import Field
from ..base import ValueObject, ResourceReference

class Assignment(ValueObject):
    """
    Penugasan sebuah Task kepada seorang Worker.
    """
    task_ref: ResourceReference = Field(..., description="The task to execute")
    worker_ref: ResourceReference = Field(..., description="The assigned agent")
    is_active: bool = Field(default=True, description="Whether this assignment is current")
