import pytest
from core.kernel.sys_platform.base import RuntimeDescriptor, RuntimeContext
from core.kernel.sys_platform.health import LifecycleState, HealthState, DependencyImpactEvaluator
from core.kernel.sys_platform.graph import RuntimeGraph, RuntimeDependencyError
from core.kernel.sys_platform.registry import RuntimeRegistry, CapabilityRegistry
from core.kernel.sys_platform.resolution import CapabilityResolver, CapabilityDescriptor, CapabilityResolutionError
from core.kernel.sys_platform.manager import RuntimeManager
from core.kernel.sys_platform.bootstrap import BootstrapEngine, BootstrapError

def test_graph_topological_sort() -> None:
    graph = RuntimeGraph()
    graph.add_dependency("workspace", "repository")
    graph.add_dependency("repository", "storage")
    
    order = graph.validate_and_sort()
    assert order == ["storage", "repository", "workspace"]

def test_graph_cycle_detection() -> None:
    graph = RuntimeGraph()
    graph.add_dependency("A", "B")
    graph.add_dependency("B", "C")
    graph.add_dependency("C", "A")
    
    with pytest.raises(RuntimeDependencyError):
        graph.validate_and_sort()

def test_derived_health_evaluation() -> None:
    desc = RuntimeDescriptor(
        runtime_id="workspace",
        display_name="Workspace Runtime",
        version="1.0.0",
        api_version="1.0.0",
        description="Test",
        author="Test",
        license="MIT",
        tags=[],
        provides=[],
        requires=["storage.read", "storage.write"],
        configuration_schema={}
    )
    
    health_healthy = DependencyImpactEvaluator.evaluate_derived_health(desc, [], [])
    assert health_healthy == HealthState.HEALTHY
    
    health_degraded = DependencyImpactEvaluator.evaluate_derived_health(desc, ["storage.write"], ["storage.read"])
    assert health_degraded == HealthState.DEGRADED
    
    health_failed = DependencyImpactEvaluator.evaluate_derived_health(desc, ["storage.read"], ["storage.read"])
    assert health_failed == HealthState.FAILED

def test_resolver_capability() -> None:
    registry = CapabilityRegistry()
    resolver = CapabilityResolver(registry)
    
    cap = CapabilityDescriptor(
        id="storage.read",
        name="Storage Read",
        version="1.0.0",
        provider="storage",
        contract="StorageReaderProtocol",
        optional=False,
        critical=True
    )
    
    resolver.register_capability_descriptor(cap)
    resolved = resolver.resolve_capability("storage.read")
    
    assert resolved.provider == "storage"
    assert registry.get_provider("storage.read") == "storage"
    
    with pytest.raises(CapabilityResolutionError):
        resolver.resolve_capability("non_existent")

def test_bootstrap_engine_success() -> None:
    registry = RuntimeRegistry()
    resolver = CapabilityResolver(CapabilityRegistry())
    manager = RuntimeManager()
    graph = RuntimeGraph()
    
    engine = BootstrapEngine(registry, resolver, manager, graph)
    
    storage_desc = RuntimeDescriptor(
        runtime_id="storage",
        display_name="Storage",
        version="1.0.0",
        api_version="1.0.0",
        description="Storage",
        author="Test",
        license="MIT",
        tags=[],
        provides=["storage.read"],
        requires=[],
        configuration_schema={}
    )
    
    repo_desc = RuntimeDescriptor(
        runtime_id="repo",
        display_name="Repo",
        version="1.0.0",
        api_version="1.0.0",
        description="Repo",
        author="Test",
        license="MIT",
        tags=[],
        provides=[],
        requires=["storage.read"],
        configuration_schema={}
    )
    
    cap = CapabilityDescriptor(
        id="storage.read",
        name="Read",
        version="1.0.0",
        provider="storage",
        contract="ReadContract",
        optional=False,
        critical=True
    )
    
    context = RuntimeContext(
        logger=None,
        configuration={},
        kernel=None,
        clock=None,
        metrics=None,
        event_bus=None,
        cancellation_token=None
    )
    
    engine.bootstrap(
        descriptors=[storage_desc, repo_desc],
        capabilities=[cap],
        instances={"storage": object(), "repo": object()},
        context=context
    )
    
    assert registry.get_state("storage").lifecycle_state == LifecycleState.READY
    assert registry.get_state("repo").lifecycle_state == LifecycleState.READY
