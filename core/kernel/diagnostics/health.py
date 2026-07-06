from enum import StrEnum
from typing import Dict, Any
from pydantic import BaseModel, Field


class HealthStatus(StrEnum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    MAINTENANCE = "maintenance"
    FAILED = "failed"


class HealthModel(BaseModel):
    status: HealthStatus = Field(default=HealthStatus.HEALTHY)
    message: str = Field(default="All systems operational")
    last_check: str = Field(default="")
    details: Dict[str, Any] = Field(default_factory=dict)
