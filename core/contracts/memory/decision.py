from pydantic import Field
from enum import StrEnum
from ..base import Entity


class DecisionStatus(StrEnum):
    PROPOSED = "proposed"
    ACCEPTED = "accepted"
    DEPRECATED = "deprecated"
    REJECTED = "rejected"


class ArchitectureDecision(Entity):
    """
    Representasi dari Architecture Decision Record (ADR) dalam bentuk terstruktur.
    """

    title: str = Field(..., description="Decision title")
    context: str = Field(..., description="Background and problem statement")
    decision: str = Field(..., description="The chosen solution")
    consequences: str = Field(..., description="Trade-offs and results")
    status: DecisionStatus = Field(
        default=DecisionStatus.PROPOSED, description="Current ADR status"
    )
