from pydantic import Field
from enum import StrEnum
from datetime import datetime
from ..base import ValueObject

class SchedulingPolicy(StrEnum):
    FIFO = "fifo"
    PRIORITY = "priority"
    ROUND_ROBIN = "round_robin"
    COST_OPTIMIZED = "cost_optimized"

class Schedule(ValueObject):
    """
    Kontrak data murni untuk penjadwalan.
    (Bukan service/engine Scheduler).
    """
    policy: SchedulingPolicy = Field(default=SchedulingPolicy.FIFO, description="Rule for executing the job")
    cron_expression: str | None = Field(default=None, description="Optional cron schedule")
    execute_after: datetime | None = Field(default=None, description="Execute strictly after this time")
    priority_level: int = Field(default=0, description="Higher integer means higher priority")
