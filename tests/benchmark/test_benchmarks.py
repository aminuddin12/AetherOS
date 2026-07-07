import pytest
from core.kernel.dependency_injection.container import ServiceContainer
from core.kernel.dependency_injection.scope import ServiceScope

class DummyService:
    pass

def test_benchmark_di_resolution(benchmark):
    container = ServiceContainer()
    container.register(DummyService, scope=ServiceScope.SINGLETON)
    
    result = benchmark(container.resolve, DummyService)
    assert isinstance(result, DummyService)

def test_benchmark_registry_lookup(benchmark):
    from core.kernel.registry.composite import CompositeRegistry
    registry = CompositeRegistry()
    registry.workers.register("key", "value")
    
    result = benchmark(registry.workers.find, "key")
    assert result == "value"
