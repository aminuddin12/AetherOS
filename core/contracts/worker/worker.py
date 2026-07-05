from pydantic import Field
from ..base import AggregateRoot
from ..identity import Principal
from .role import Role
from .capability_profile import CapabilityProfile
from .reputation import ReputationScore
from .lifecycle import WorkerLifecycle

class Worker(AggregateRoot):
    """
    Entitas utama (Aggregate) yang mewakili satu Agent di AetherOS.
    """
    principal: Principal = Field(..., description="Identity mapping for this worker")
    role: Role = Field(..., description="Assigned role (persona)")
    profile: CapabilityProfile = Field(default_factory=CapabilityProfile, description="Capabilities")
    reputation: ReputationScore = Field(default_factory=ReputationScore, description="Performance metrics")
    lifecycle: WorkerLifecycle = Field(default_factory=WorkerLifecycle, description="Current state")
