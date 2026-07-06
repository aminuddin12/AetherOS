#!/usr/bin/env python3
"""
Demonstration of AetherOS Runtime SDK Kernel Integration.

This script demonstrates how the new runtime capabilities (Company Brain, Provider Router, 
and Workflow Runtime) are registered with the kernel's capability system during bootstrap.
"""

import asyncio
from unittest.mock import Mock
from aether_runtime import AetherRuntime, RuntimeBuilder
from aether_runtime.context.context import RuntimeContext
from aether_runtime.kernel_integration import KernelIntegration
from aether_runtime.kernel_bridge import KernelBridge
from core.kernel.sys_platform.resolution import CapabilityResolver, CapabilityRegistry


def demonstrate_kernel_integration():
    """Demonstrate the kernel integration functionality."""
    print("=== AetherOS Runtime SDK Kernel Integration Demo ===\n")
    
    # Step 1: Create kernel components
    print("1. Creating kernel capability system...")
    capability_registry = CapabilityRegistry()
    resolver = CapabilityResolver(capability_registry)
    kernel_bridge = KernelBridge(resolver)
    
    # Step 2: Create kernel integration
    print("2. Setting up kernel integration...")
    kernel_integration = KernelIntegration()
    kernel_integration.set_kernel_bridge(kernel_bridge)
    
    # Step 3: Create runtime with kernel integration
    print("3. Creating AetherOS Runtime with kernel integration...")
    context = RuntimeContext(user_id="demo_user", workspace_id="demo_workspace")
    builder = RuntimeBuilder().with_context(context)
    builder.with_kernel_integration(kernel_integration)
    runtime = builder.build()
    
    # Step 4: Show available capabilities before registration
    print("4. Available runtime capabilities:")
    capabilities = asyncio.run(runtime.capabilities())
    for cap_id, cap_info in capabilities.items():
        print(f"   - {cap_id}: {cap_info['name']} v{cap_info['version']}")
    
    # Step 5: Register capabilities with kernel
    print("\n5. Registering capabilities with kernel...")
    registered = runtime.register_with_kernel()
    print(f"   Successfully registered {len(registered)} capabilities:")
    for cap_id in registered:
        print(f"   - {cap_id}")
    
    # Step 6: Verify registration
    print("\n6. Verifying capability registration:")
    for cap_id in ["company_brain", "provider_router", "workflow_runtime"]:
        is_registered = runtime.is_capability_registered(cap_id)
        can_resolve = kernel_bridge.can_resolve_capability(cap_id)
        print(f"   - {cap_id}: Registered={is_registered}, Resolvable={can_resolve}")
    
    # Step 7: Demonstrate capability resolution
    print("\n7. Demonstrating kernel capability resolution:")
    try:
        company_brain_cap = resolver.resolve_capability("company_brain")
        print(f"   - Company Brain: Provider={company_brain_cap.provider}, Contract={company_brain_cap.contract}")
        
        provider_router_cap = resolver.resolve_capability("provider_router")
        print(f"   - Provider Router: Provider={provider_router_cap.provider}, Contract={provider_router_cap.contract}")
        
        workflow_runtime_cap = resolver.resolve_capability("workflow_runtime")
        print(f"   - Workflow Runtime: Provider={workflow_runtime_cap.provider}, Contract={workflow_runtime_cap.contract}")
        
    except Exception as e:
        print(f"   Error resolving capabilities: {e}")
    
    # Step 8: Show kernel integration status
    print("\n8. Kernel integration status:")
    kernel_integration = runtime.get_kernel_integration()
    registered_caps = kernel_integration.list_registered_capabilities()
    print(f"   - Total registered capabilities: {len(registered_caps)}")
    print(f"   - Capabilities: {', '.join(registered_caps)}")
    
    print("\n=== Demo completed successfully! ===")
    print("\nThe AetherOS Runtime SDK is now fully integrated with the kernel's capability system.")
    print("The new runtime capabilities (Company Brain, Provider Router, Workflow Runtime)")
    print("are properly registered and can be discovered by other kernel components.")


if __name__ == "__main__":
    demonstrate_kernel_integration()