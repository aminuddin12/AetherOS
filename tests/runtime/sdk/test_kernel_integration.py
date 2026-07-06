import pytest
from unittest.mock import Mock, MagicMock
from aether_runtime import AetherRuntime, RuntimeBuilder
from aether_runtime.context.context import RuntimeContext
from aether_runtime.kernel_integration import KernelIntegration
from aether_runtime.kernel_bridge import KernelBridge
from aether_runtime.capabilities import RuntimeCapabilities
from core.kernel.sys_platform.resolution import CapabilityResolver, CapabilityRegistry


@pytest.mark.asyncio
async def test_capability_descriptors():
    """Test that capability descriptors are properly defined."""
    capabilities = RuntimeCapabilities.get_capability_descriptors()
    
    # Should have 3 capabilities
    assert len(capabilities) == 3
    
    # Check each capability
    capability_ids = [cap.id for cap in capabilities]
    assert "company_brain" in capability_ids
    assert "provider_router" in capability_ids
    assert "workflow_runtime" in capability_ids
    
    # Check Company Brain capability
    company_brain = next(cap for cap in capabilities if cap.id == "company_brain")
    assert company_brain.name == "Company Brain"
    assert company_brain.version == "1.0.0"
    assert company_brain.provider == "aether_runtime"
    assert company_brain.contract == "CompanyBrainProtocol"
    assert company_brain.critical == True
    assert company_brain.optional == False
    
    # Check Provider Router capability
    provider_router = next(cap for cap in capabilities if cap.id == "provider_router")
    assert provider_router.name == "Provider Router"
    assert provider_router.version == "1.0.0"
    assert provider_router.provider == "aether_runtime"
    assert provider_router.contract == "ProviderRouterProtocol"
    assert provider_router.critical == True
    
    # Check Workflow Runtime capability
    workflow_runtime = next(cap for cap in capabilities if cap.id == "workflow_runtime")
    assert workflow_runtime.name == "Workflow Runtime"
    assert workflow_runtime.version == "1.0.0"
    assert workflow_runtime.provider == "aether_runtime"
    assert workflow_runtime.contract == "WorkflowRuntimeProtocol"
    assert workflow_runtime.critical == True


@pytest.mark.asyncio
async def test_kernel_integration_initialization():
    """Test kernel integration initialization."""
    integration = KernelIntegration()
    
    # Initially no capabilities should be registered
    assert integration.list_registered_capabilities() == []
    assert integration.is_capability_registered("company_brain") == False
    
    # Should raise error if trying to register without kernel bridge
    with pytest.raises(RuntimeError):
        integration.register_capabilities()


@pytest.mark.asyncio
async def test_kernel_bridge_integration():
    """Test kernel bridge integration with mock kernel."""
    # Create mock capability resolver
    mock_resolver = Mock(spec=CapabilityResolver)
    mock_resolver.register_capability_descriptor = Mock()
    
    # Create kernel bridge
    kernel_bridge = KernelBridge(mock_resolver)
    
    # Create kernel integration and set bridge
    integration = KernelIntegration()
    integration.set_kernel_bridge(kernel_bridge)
    
    # Register capabilities
    registered = integration.register_capabilities()
    
    # Should have registered 3 capabilities
    assert len(registered) == 3
    assert "company_brain" in registered
    assert "provider_router" in registered
    assert "workflow_runtime" in registered
    
    # Check that capabilities are now registered
    assert integration.is_capability_registered("company_brain") == True
    assert integration.is_capability_registered("provider_router") == True
    assert integration.is_capability_registered("workflow_runtime") == True
    assert integration.is_capability_registered("nonexistent") == False
    
    # Check that register_capability_descriptor was called 3 times
    assert mock_resolver.register_capability_descriptor.call_count == 3


@pytest.mark.asyncio
async def test_runtime_kernel_registration():
    """Test runtime SDK kernel registration functionality."""
    # Create mock capability resolver
    mock_resolver = Mock(spec=CapabilityResolver)
    mock_resolver.register_capability_descriptor = Mock()
    
    # Create kernel bridge
    kernel_bridge = KernelBridge(mock_resolver)
    
    # Create runtime with kernel integration
    context = RuntimeContext(user_id="tester", workspace_id="w-001")
    builder = RuntimeBuilder().with_context(context)
    integration = KernelIntegration()
    integration.set_kernel_bridge(kernel_bridge)
    builder.with_kernel_integration(integration)
    
    runtime = builder.build()
    
    # Register capabilities
    registered = runtime.register_with_kernel()
    
    # Should have registered 3 capabilities
    assert len(registered) == 3
    assert "company_brain" in registered
    assert "provider_router" in registered
    assert "workflow_runtime" in registered
    
    # Check that capabilities are registered
    assert runtime.is_capability_registered("company_brain") == True
    assert runtime.is_capability_registered("provider_router") == True
    assert runtime.is_capability_registered("workflow_runtime") == True
    assert runtime.is_capability_registered("nonexistent") == False
    
    # Check kernel integration object
    kernel_integration = runtime.get_kernel_integration()
    assert kernel_integration is not None
    assert kernel_integration.list_registered_capabilities() == registered


@pytest.mark.asyncio
async def test_capabilities_method():
    """Test the capabilities() method returns proper descriptors."""
    runtime = RuntimeBuilder().build()
    
    capabilities = await runtime.capabilities()
    
    # Should return dictionary with 3 capabilities
    assert len(capabilities) == 3
    assert "company_brain" in capabilities
    assert "provider_router" in capabilities
    assert "workflow_runtime" in capabilities
    
    # Check Company Brain capability structure
    company_brain = capabilities["company_brain"]
    assert company_brain["name"] == "Company Brain"
    assert company_brain["version"] == "1.0.0"
    assert company_brain["provider"] == "aether_runtime"
    assert company_brain["contract"] == "CompanyBrainProtocol"
    assert company_brain["critical"] == True
    assert company_brain["optional"] == False
    assert "description" in company_brain


@pytest.mark.asyncio
async def test_kernel_bridge_error_handling():
    """Test error handling in kernel bridge."""
    # Create mock resolver that raises exception
    mock_resolver = Mock(spec=CapabilityResolver)
    mock_resolver.register_capability_descriptor = Mock(side_effect=Exception("Registration failed"))
    
    # Create kernel bridge and integration
    kernel_bridge = KernelBridge(mock_resolver)
    integration = KernelIntegration()
    integration.set_kernel_bridge(kernel_bridge)
    
    # Should handle registration errors gracefully
    registered = integration.register_capabilities()
    
    # Should have registered 0 capabilities due to error
    assert len(registered) == 0
    
    # Check that no capabilities are registered
    assert integration.list_registered_capabilities() == []


@pytest.mark.asyncio
async def test_runtime_without_kernel_integration():
    """Test runtime behavior when kernel integration is not initialized."""
    runtime = RuntimeBuilder().build()
    
    # Should raise error when trying to register without kernel integration
    with pytest.raises(RuntimeError):
        runtime.register_with_kernel()
    
    # Should return False for capability checks
    assert runtime.is_capability_registered("company_brain") == False
    
    # Should still be able to get capabilities (they exist, just not registered)
    capabilities = await runtime.capabilities()
    assert len(capabilities) == 3