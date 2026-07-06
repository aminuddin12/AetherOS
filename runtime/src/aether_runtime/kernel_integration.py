"""
Kernel integration module for AetherOS runtime SDK.
Handles capability registration and kernel bootstrap integration.
"""

from typing import List, Dict, Any, Optional
from .capabilities import RuntimeCapabilities, RuntimeCapability
from .kernel_bridge import KernelBridge


class KernelIntegration:
    """
    Handles integration between the AetherOS runtime SDK and the kernel's capability system.
    """
    
    def __init__(self):
        self._registered_capabilities = {}
        self._kernel_bridge = None
    
    def set_kernel_bridge(self, kernel_bridge: KernelBridge):
        """
        Set the kernel bridge for capability registration.
        
        Args:
            kernel_bridge: The kernel bridge object that provides capability registration methods.
        """
        self._kernel_bridge = kernel_bridge
    
    def register_capabilities(self) -> List[str]:
        """
        Register all runtime capabilities with the kernel.
        
        Returns:
            List of successfully registered capability IDs.
        """
        if not self._kernel_bridge:
            raise RuntimeError("Kernel bridge not initialized. Call set_kernel_bridge() first.")
        
        registered = []
        capabilities = RuntimeCapabilities.get_capability_descriptors()
        
        for capability in capabilities:
            try:
                # Convert our RuntimeCapability to kernel's CapabilityDescriptor format
                kernel_descriptor = self._convert_to_kernel_descriptor(capability)
                
                # Register with kernel
                self._kernel_bridge.register_capability_descriptor(kernel_descriptor)
                self._registered_capabilities[capability.id] = capability
                registered.append(capability.id)
                
            except Exception as e:
                # Log error but continue with other capabilities
                print(f"Failed to register capability {capability.id}: {e}")
                continue
        
        return registered
    
    def _convert_to_kernel_descriptor(self, capability: RuntimeCapability) -> Dict[str, Any]:
        """
        Convert RuntimeCapability to kernel's CapabilityDescriptor format.
        """
        return {
            "id": capability.id,
            "name": capability.name,
            "version": capability.version,
            "provider": capability.provider,
            "contract": capability.contract,
            "optional": capability.optional,
            "critical": capability.critical
        }
    
    def get_registered_capability(self, capability_id: str) -> Optional[RuntimeCapability]:
        """
        Get a registered capability by ID.
        
        Args:
            capability_id: The ID of the capability to retrieve.
            
        Returns:
            The RuntimeCapability object if found, None otherwise.
        """
        return self._registered_capabilities.get(capability_id)
    
    def list_registered_capabilities(self) -> List[str]:
        """
        List all registered capability IDs.
        
        Returns:
            List of registered capability IDs.
        """
        return list(self._registered_capabilities.keys())
    
    def unregister_capability(self, capability_id: str) -> bool:
        """
        Unregister a capability.
        
        Args:
            capability_id: The ID of the capability to unregister.
            
        Returns:
            True if capability was unregistered, False if it wasn't registered.
        """
        if capability_id not in self._registered_capabilities:
            return False
        
        del self._registered_capabilities[capability_id]
        return True
    
    def is_capability_registered(self, capability_id: str) -> bool:
        """
        Check if a capability is registered.
        
        Args:
            capability_id: The ID of the capability to check.
            
        Returns:
            True if capability is registered, False otherwise.
        """
        return capability_id in self._registered_capabilities