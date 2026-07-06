"""
Kernel bridge module that adapts the AetherOS runtime SDK to work with the kernel's capability system.
"""

from typing import Dict, Any, List
from core.kernel.sys_platform.resolution import CapabilityDescriptor as KernelCapabilityDescriptor


class KernelBridge:
    """
    Bridge between AetherOS runtime SDK and the kernel's capability system.
    Provides the interface needed by KernelIntegration to register capabilities.
    """
    
    def __init__(self, capability_resolver):
        """
        Initialize the kernel bridge.
        
        Args:
            capability_resolver: The kernel's CapabilityResolver instance.
        """
        self._capability_resolver = capability_resolver
    
    def register_capability_descriptor(self, descriptor: Dict[str, Any]) -> None:
        """
        Register a capability descriptor with the kernel.
        
        Args:
            descriptor: Dictionary containing capability descriptor information.
        """
        # Convert dictionary to kernel's CapabilityDescriptor
        kernel_descriptor = KernelCapabilityDescriptor(
            id=descriptor["id"],
            name=descriptor["name"],
            version=descriptor["version"],
            provider=descriptor["provider"],
            contract=descriptor["contract"],
            optional=descriptor.get("optional", False),
            critical=descriptor.get("critical", False)
        )
        
        # Register with the kernel's resolver
        self._capability_resolver.register_capability_descriptor(kernel_descriptor)
    
    def get_registered_capabilities(self) -> List[str]:
        """
        Get list of registered capability IDs.
        
        Returns:
            List of capability IDs that have been registered.
        """
        # The kernel's resolver doesn't directly expose this, but we can
        # work around it by trying to resolve known capability IDs
        return []  # This would need to be enhanced in the kernel
    
    def can_resolve_capability(self, capability_id: str) -> bool:
        """
        Check if a capability can be resolved.
        
        Args:
            capability_id: The capability ID to check.
            
        Returns:
            True if capability can be resolved, False otherwise.
        """
        try:
            self._capability_resolver.resolve_capability(capability_id)
            return True
        except Exception:
            return False