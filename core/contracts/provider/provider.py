from pydantic import Field
from typing import Any
from ..base import Entity, ContractProtocol
from .provider_capability import ProviderCapability
from .provider_limits import ProviderLimits
from .provider_pricing import ProviderPricing
from .provider_health import ProviderHealth

class ProviderEntity(Entity):
    """
    Data registry untuk satu model/vendor (mis: 'gpt-4o', 'claude-3-5-sonnet').
    """
    name: str = Field(..., description="Model identifier")
    vendor: str = Field(..., description="Vendor name (e.g., 'openai')")
    capability: ProviderCapability = Field(..., description="Supported features")
    limits: ProviderLimits = Field(..., description="Quotas")
    pricing: ProviderPricing = Field(..., description="Cost calculation")
    health: ProviderHealth = Field(default_factory=ProviderHealth, description="Current availability")

class ProviderProtocol(ContractProtocol):
    """
    Abstraksi murni eksekutor LLM (Port di arsitektur Hexagonal).
    """
    async def invoke(self, payload: Any, provider_ref: ProviderEntity) -> Any:
        ...
