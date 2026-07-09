from __future__ import annotations

from ..core.provider import StorageProvider


class AdapterRegistry:
    def __init__(self) -> None:
        self._registry: dict[str, type[StorageProvider]] = {}

    def register(self, scheme: str, provider_cls: type[StorageProvider]) -> None:
        self._registry[scheme] = provider_cls

    def get(self, scheme: str) -> type[StorageProvider] | None:
        return self._registry.get(scheme)

    def list_schemes(self) -> list[str]:
        return list(self._registry.keys())


registry = AdapterRegistry()
