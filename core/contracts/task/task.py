from enum import StrEnum
from typing import List
from pydantic import Field
from ..base import AggregateRoot, ResourceReference


class TaskStatus(StrEnum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    IN_REVIEW = "in_review"
    COMPLETED = "completed"
    FAILED = "failed"


class Task(AggregateRoot):
    """
    Unit kerja terdiskrit (seperti tiket JIRA) di dalam organisasi.
    """

    title: str = Field(..., description="Task title")
    description: str = Field(..., description="Detailed instructions")
    status: TaskStatus = Field(default=TaskStatus.PENDING, description="Current execution status")
    creator_ref: ResourceReference = Field(
        ..., description="Reference to who created the task (Principal/User)"
    )
    dependencies: List[ResourceReference] = Field(
        default_factory=list, description="References to blocking tasks"
    )
