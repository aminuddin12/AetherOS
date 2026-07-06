from pydantic import Field
from ..base import ValueObject


class ReputationScore(ValueObject):
    """
    Metrik kinerja agen (Agent Reputation) untuk auto-routing.
    """

    performance: float = Field(default=0.0, description="Task success rate")
    reliability: float = Field(default=0.0, description="Failure/Loop rate")
    security: float = Field(default=0.0, description="Security vulnerability rate")
    speed: float = Field(default=0.0, description="Task execution latency")
    cost_efficiency: float = Field(default=0.0, description="Token usage efficiency")
    teamwork: float = Field(default=0.0, description="Handover success rate")
