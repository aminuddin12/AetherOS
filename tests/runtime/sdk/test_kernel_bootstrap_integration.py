"""
Integration tests for kernel bootstrap with runtime capabilities.
Tests the full integration between runtime SDK and kernel platform bootstrap.
"""

import pytest
from unittest.mock import Mock
from aether_runtime import AetherRuntime, RuntimeBuilder
from aether_runtime.context.context import RuntimeContext
from aether_runtime.kernel_integration import KernelIntegration
from aether_runtime.kernel_bridge import KernelBridge
from core.kernel.sys_platform.bootstrap import BootstrapEngine
from core.kernel.sys_platform.registry import RuntimeRegistry, CapabilityRegistry
from core.kernel.sys_platform.resolution import CapabilityResolver
from core.kernel.sys_platform.manager import RuntimeManager
from core.kernel.sys_platform.graph import RuntimeGraph
from core.kernel.sys_platform.base import RuntimeDescriptor, RuntimeState, RuntimeContext as KernelRuntimeContext
from core.kernel.sys_platform.health import LifecycleState, HealthState


@pytest.mark.asyncio
async def test_full_kernel_bootstrap_integration():
    """
    Test the complete kernel bootstrap integration with runtime capabilities.
    This simulates the full bootstrap process that would occur in production.
    """
    # Step 1: Create kernel components
    runtime_registry = RuntimeRegistry()
    capability_registry = CapabilityRegistry()
    resolver = CapabilityResolver(capability_registry)
    manager = RuntimeManager()
    graph = RuntimeGraph()
    
    # Step 2: Create kernel bridge and integration
    kernel_bridge = KernelBridge(resolver)
    kernel_integration = KernelIntegration()
    kernel_integration.set_kernel_bridge(kernel_bridge)
    
    # Step 3: Create runtime with kernel integration
    context = RuntimeContext(user_id="test_user", workspace_id="test_workspace")
    builder = RuntimeBuilder().with_context(context)
    builder.with_kernel_integration(kernel_integration)
    runtime = builder.build()
    
    # Step 4: Register runtime capabilities with kernel
    registered_capabilities = runtime.register_with_kernel()
    
    # Verify capabilities were registered
    assert len(registered_capabilities) == 3
    assert "company_brain" in registered_capabilities
    assert "provider_router" in registered_capabilities
    assert "workflow_runtime" in registered_capabilities
    
    # Step 5: Create kernel bootstrap engine
    bootstrap_engine = BootstrapEngine(runtime_registry, resolver, manager, graph)
    
    # Step 6: Create runtime descriptors for kernel bootstrap
    # Runtime that provides the capabilities
    runtime_descriptor = RuntimeDescriptor(
        runtime_id="aether_runtime",
        display_name="Aether Runtime",
        version="1.0.0",
        api_version="1.0.0",
        description="AetherOS Runtime SDK",
        author="AetherOS",
        license="MIT",
        tags=["runtime", "sdk"],
        provides=[
            "company_brain",
            "provider_router", 
            "workflow_runtime"
        ],
        requires=[],
        configuration_schema={}
    )
    
    # Runtime that depends on the capabilities
    dependent_runtime_descriptor = RuntimeDescriptor(
        runtime_id="dependent_runtime",
        display_name="Dependent Runtime",
        version="1.0.0",
        api_version="1.0.0",
        description="Runtime that depends on Aether capabilities",
        author="Test",
        license="MIT",
        tags=["test"],
        provides=[],
        requires=[
            "company_brain",
            "provider_router"
        ],
        configuration_schema={}
    )
    
    # Step 7: Create kernel runtime context
    kernel_context = KernelRuntimeContext(
        logger=Mock(),
        configuration={},
        kernel=Mock(),
        clock=Mock(),
        metrics=Mock(),
        event_bus=Mock(),
        cancellation_token=Mock()
    )
    
    # Step 8: Bootstrap the kernel with runtime capabilities
    bootstrap_engine.bootstrap(
        descriptors=[runtime_descriptor, dependent_runtime_descriptor],
        capabilities=[],  # Capabilities already registered via runtime
        instances={
            "aether_runtime": runtime,
            "dependent_runtime": Mock()
        },
        context=kernel_context
    )
    
    # Step 9: Verify bootstrap was successful
    # Check that runtimes are registered
    assert runtime_registry.get_descriptor("aether_runtime") is not None
    assert runtime_registry.get_descriptor("dependent_runtime") is not None
    
    # Check that capabilities can be resolved
    assert resolver.resolve_capability("company_brain").provider == "aether_runtime"
    assert resolver.resolve_capability("provider_router").provider == "aether_runtime"
    assert resolver.resolve_capability("workflow_runtime").provider == "aether_runtime"
    
    # Check that runtime states are READY
    runtime_state = runtime_registry.get_state("aether_runtime")
    assert runtime_state.lifecycle_state == LifecycleState.READY
    
    dependent_state = runtime_registry.get_state("dependent_runtime")
    assert dependent_state.lifecycle_state == LifecycleState.READY
    
    # Step 10: Verify runtime can still function normally
    capabilities = await runtime.capabilities()
    assert len(capabilities) == 3
    assert runtime.is_capability_registered("company_brain") == True
    assert runtime.is_capability_registered("provider_router") == True
    assert runtime.is_capability_registered("workflow_runtime") == True


@pytest.mark.asyncio
async def test_kernel_bootstrap_with_missing_capability():
    """
    Test bootstrap behavior when a required capability is missing.
    """
    # Create kernel components
    runtime_registry = RuntimeRegistry()
    capability_registry = CapabilityRegistry()
    resolver = CapabilityResolver(capability_registry)
    manager = RuntimeManager()
    graph = RuntimeGraph()
    
    # Create kernel bridge and integration
    kernel_bridge = KernelBridge(resolver)
    kernel_integration = KernelIntegration()
    kernel_integration.set_kernel_bridge(kernel_bridge)
    
    # Create runtime and register only some capabilities
    runtime = RuntimeBuilder().build()
    runtime._kernel_integration = kernel_integration
    
    # Manually register only company_brain capability
    from aether_runtime.capabilities import RuntimeCapabilities
    company_brain = RuntimeCapabilities._company_brain_capability()
    kernel_bridge.register_capability_descriptor({
        "id": company_brain.id,
        "name": company_brain.name,
        "version": company_brain.version,
        "provider": company_brain.provider,
        "contract": company_brain.contract,
        "optional": company_brain.optional,
        "critical": company_brain.critical
    })
    
    # Create bootstrap engine
    bootstrap_engine = BootstrapEngine(runtime_registry, resolver, manager, graph)
    
    # Create runtime descriptor that requires missing capability
    runtime_descriptor = RuntimeDescriptor(
        runtime_id="test_runtime",
        display_name="Test Runtime",
        version="1.0.0",
        api_version="1.0.0",
        description="Test Runtime",
        author="Test",
        license="MIT",
        tags=[],
        provides=[],
        requires=["provider_router"],  # This capability is not registered
        configuration_schema={}
    )
    
    kernel_context = KernelRuntimeContext(
        logger=Mock(),
        configuration={},
        kernel=Mock(),
        clock=Mock(),
        metrics=Mock(),
        event_bus=Mock(),
        cancellation_token=Mock()
    )
    
    # Bootstrap should fail due to missing capability
    with pytest.raises(Exception) as exc_info:
        bootstrap_engine.bootstrap(
            descriptors=[runtime_descriptor],
            capabilities=[],
            instances={"test_runtime": Mock()},
            context=kernel_context
        )
    
    # Verify the error is about capability resolution
    assert "Failed resolving requirement" in str(exc_info.value)
    assert "provider_router" in str(exc_info.value)


@pytest.mark.asyncio
async def test_capability_discovery_and_registration():
    """
    Test that capabilities can be discovered and registered properly."""
    # Create kernel components
    capability_registry = CapabilityRegistry()
    resolver = CapabilityResolver(capability_registry)
    kernel_bridge = KernelBridge(resolver)
    
    # Create runtime and register capabilities
    runtime = RuntimeBuilder().build()
    integration = KernelIntegration()
    integration.set_kernel_bridge(kernel_bridge)
    runtime._kernel_integration = integration
    
    registered = runtime.register_with_kernel()
    
    # Verify capabilities are registered in kernel
    assert resolver.resolve_capability("company_brain").provider == "aether_runtime"
    assert resolver.resolve_capability("provider_router").provider == "aether_runtime"
    assert resolver.resolve_capability("workflow_runtime").provider == "aether_runtime"
    
    # Verify capability registry has the mappings
    assert capability_registry.get_provider("company_brain") == "aether_runtime"
    assert capability_registry.get_provider("provider_router") == "aether_runtime"
    assert capability_registry.get_provider("workflow_runtime") == "aether_runtime"
    
    # Verify runtime can check registration status
    assert runtime.is_capability_registered("company_brain") == True
    assert runtime.is_capability_registered("nonexistent") == False