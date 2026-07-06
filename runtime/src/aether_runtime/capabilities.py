from typing import List
from pydantic import BaseModel

class RuntimeCapability(BaseModel):
    """
    Descriptor for runtime capabilities that can be registered with the kernel.
    """
    id: str
    name: str
    version: str
    provider: str
    contract: str
    optional: bool = False
    critical: bool = False
    description: str = ""

class RuntimeCapabilities:
    """
    Collection of runtime capabilities for the AetherOS runtime SDK.
    """
    
    @staticmethod
    def get_capability_descriptors() -> List[RuntimeCapability]:
        """
        Get all capability descriptors for the runtime SDK.
        """
        return [
            RuntimeCapabilities._company_brain_capability(),
            RuntimeCapabilities._provider_router_capability(),
            RuntimeCapabilities._workflow_runtime_capability(),
        ]
    
    @staticmethod
    def _company_brain_capability() -> RuntimeCapability:
        """
        Company Brain capability descriptor.
        Provides knowledge management and indexing capabilities.
        """
        return RuntimeCapability(
            id="company_brain",
            name="Company Brain",
            version="1.0.0",
            provider="aether_runtime",
            contract="CompanyBrainProtocol",
            optional=False,
            critical=True,
            description="Knowledge management and indexing system for organizational knowledge"
        )
    
    @staticmethod
    def _provider_router_capability() -> RuntimeCapability:
        """
        Provider Router capability descriptor.
        Provides provider selection and routing capabilities.
        """
        return RuntimeCapability(
            id="provider_router",
            name="Provider Router",
            version="1.0.0",
            provider="aether_runtime",
            contract="ProviderRouterProtocol",
            optional=False,
            critical=True,
            description="Dynamic provider selection and routing system"
        )
    
    @staticmethod
    def _workflow_runtime_capability() -> RuntimeCapability:
        """
        Workflow Runtime capability descriptor.
        Provides workflow execution and management capabilities.
        """
        return RuntimeCapability(
            id="workflow_runtime",
            name="Workflow Runtime",
            version="1.0.0",
            provider="aether_runtime",
            contract="WorkflowRuntimeProtocol",
            optional=False,
            critical=True,
            description="Workflow execution and lifecycle management system"
        )