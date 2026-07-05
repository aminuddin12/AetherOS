from pydantic import Field
from ..base import ValueObject

class Assignment(ValueObject):
    """
    Penugasan sebuah Task kepada seorang Worker.
    """
    task_id: str = Field(..., description="The task to execute")
    worker_id: str = Field(..., description="The assigned agent")
    is_active: bool = Field(default=True, description="Whether this assignment is current")
