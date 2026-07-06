from typing import Protocol, Any, Dict

class DependencyRegistry(Protocol):
    def get(self, name: str) -> Any: ...
    def register(self, name: str, instance: Any) -> None: ...

class DefaultRegistry(DependencyRegistry):
    def __init__(self):
        self._services: Dict[str, Any] = {}
        
    def get(self, name: str) -> Any:
        return self._services.get(name)
        
    def register(self, name: str, instance: Any) -> None:
        self._services[name] = instance
