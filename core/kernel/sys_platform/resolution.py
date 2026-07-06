from pydantic import BaseModel
from typing import Dict, Any
from .registry import CapabilityRegistry

class CapabilityDescriptor(BaseModel):
    model_config = {"frozen": True}
    
    id: str
    name: str
    version: str
    provider: str
    contract: str
    optional: bool
    critical: bool

class CapabilityResolutionError(Exception):
    pass

class CapabilityResolver:
    def __init__(self, registry: CapabilityRegistry) -> None:
        self._registry = registry
        self._descriptors: Dict[str, CapabilityDescriptor] = {}

    def register_capability_descriptor(self, descriptor: CapabilityDescriptor) -> None:
        self._descriptors[descriptor.id] = descriptor
        self._registry.register_capability(descriptor.id, descriptor.provider)

    def resolve_capability(self, capability_id: str) -> CapabilityDescriptor:
        desc = self._descriptors.get(capability_id)
        if not desc:
            raise CapabilityResolutionError(f"Capability {capability_id} could not be resolved")
        return desc
