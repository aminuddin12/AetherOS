from enum import StrEnum
from pydantic import Field
from ..base import ValueObject, ResourceReference

class ApprovalStatus(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class Approval(ValueObject):
    """
    Gatekeeper (Human-in-the-Loop) persetujuan aksi kritis.
    """
    required_role: str = Field(..., description="Role required to approve")
    status: ApprovalStatus = Field(default=ApprovalStatus.PENDING)
    approved_by_ref: ResourceReference | None = Field(default=None, description="Who approved it")
