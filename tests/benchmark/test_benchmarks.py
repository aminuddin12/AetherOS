import pytest
import time
from core.kernel.dependency_injection.container import ServiceContainer
from core.kernel.dependency_injection.provider import SingletonProvider

def dummy_service():
    return "DummyService"

def test_benchmark_di_resolution(benchmark):
    container = ServiceContainer()
    provider = SingletonProvider(dummy_service)
    container.register("dummy", provider)
    
    result = benchmark(container.resolve, "dummy")
    assert result == "DummyService"

def test_benchmark_registry_lookup(benchmark):
    from core.kernel.registry.composite import CompositeRegistry
    class MockRegistry:
        def __init__(self):
            self.data = {"key": "value"}
        def get(self, key):
            return self.data.get(key)
        def register(self, key, item):
            self.data[key] = item
            
    registry = CompositeRegistry()
    registry.add_registry("mock", MockRegistry())
    
    result = benchmark(registry.get, "mock", "key")
    assert result == "value"
