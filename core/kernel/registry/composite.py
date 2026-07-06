from typing import Any, List, Dict
from .base import RegistryProtocol
import json


class BaseRegistry(RegistryProtocol):
    def __init__(self):
        self._store: Dict[str, Any] = {}

    def register(self, key: str, instance: Any) -> None:
        self._store[key] = instance

    def unregister(self, key: str) -> None:
        self._store.pop(key, None)

    def find(self, key: str) -> Any | None:
        return self._store.get(key)

    def filter(self, predicate: callable) -> List[Any]:
        return [v for v in self._store.values() if predicate(v)]

    def search(self, query: str) -> List[Any]:
        # Simple text search fallback
        return []

    def replace(self, key: str, new_instance: Any) -> None:
        if key in self._store:
            self._store[key] = new_instance

    def snapshot(self) -> Dict[str, Any]:
        return dict(self._store)

    def export(self) -> str:
        # In real scenario, needs complex serialization.
        return "{}"

    def import_data(self, data: str) -> None:
        pass


class CompositeRegistry:
    """
    Registry pusat yang mendelegasikan lookup ke sub-registries.
    """

    def __init__(self):
        self.workers = BaseRegistry()
        self.tools = BaseRegistry()
        self.providers = BaseRegistry()
        self.extensions = BaseRegistry()
