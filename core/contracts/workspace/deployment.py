from enum import StrEnum
from pydantic import Field
from ..base import DomainEvent, ResourceReference

class DeploymentStatus(StrEnum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    SUCCESS = "success"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"

class Deployment(DomainEvent):
    """
    Catatan pengiriman kode/artefak ke environment.
    """
    environment_ref: ResourceReference = Field(..., description="Target environment")
    commit_ref: ResourceReference = Field(..., description="What was deployed")
    status: DeploymentStatus = Field(default=DeploymentStatus.PENDING)
