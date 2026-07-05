from enum import StrEnum
from pydantic import Field
from ..base import ValueObject

class ProviderStatus(StrEnum):
    ONLINE = "online"
    DEGRADED = "degraded"
    OFFLINE = "offline"

class ProviderHealth(ValueObject):
    """
    Status ketersediaan provider untuk routing dinamis.
    """
    status: ProviderStatus = Field(default=ProviderStatus.ONLINE)
    latency_ms: float = Field(default=0.0, description="Average response latency")
    error_rate: float = Field(default=0.0, description="Failure percentage (0.0 - 1.0)")
