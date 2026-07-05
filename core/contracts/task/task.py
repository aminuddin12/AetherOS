from enum import StrEnum
from typing import List
from pydantic import Field
from ..base import AggregateRoot
from ..identity import Principal

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
    creator: Principal = Field(..., description="Who created the task")
    dependencies: List[str] = Field(default_factory=list, description="IDs of tasks that must finish first")
