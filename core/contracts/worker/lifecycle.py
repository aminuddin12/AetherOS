from enum import StrEnum
from pydantic import Field
from ..base import ValueObject


class LifecyclePhase(StrEnum):
    CREATED = "created"
    TRAINING = "training"
    CERTIFICATION = "certification"
    ASSIGNED = "assigned"
    WORKING = "working"
    REVIEW = "review"
    PROMOTION = "promotion"
    MENTOR = "mentor"
    RETIRED = "retired"


class WorkerLifecycle(ValueObject):
    """
    Status agen saat ini dalam Lifecycle AetherOS.
    """

    current_phase: LifecyclePhase = Field(
        default=LifecyclePhase.CREATED, description="Current lifecycle stage"
    )
    tasks_completed: int = Field(default=0, description="Total tasks completed")
    is_cleared_for_production: bool = Field(default=False, description="Has passed certification")
