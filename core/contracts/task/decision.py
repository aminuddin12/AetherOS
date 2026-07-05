from pydantic import Field
from ..base import Command
from .approval import ApprovalStatus

class Decision(Command):
    """
    Keputusan konkrit yang diambil oleh manusia saat Approval Gate.
    """
    approval_id: str = Field(..., description="Reference to the Approval requested")
    decision: ApprovalStatus = Field(..., description="The verdict")
    reasoning: str | None = Field(default=None, description="Explanation for rejection/approval")
