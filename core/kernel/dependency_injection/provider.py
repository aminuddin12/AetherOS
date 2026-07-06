from typing import Any, Callable
from .scope import ServiceScope


class ServiceProvider:
    def __init__(self, factory: Callable[..., Any], scope: ServiceScope):
        self.factory = factory
        self.scope = scope
        self.instance = None

    def get(self, resolver: "Resolver") -> Any:
        if self.scope == ServiceScope.SINGLETON:
            if self.instance is None:
                self.instance = resolver.build(self.factory)
            return self.instance
        return resolver.build(self.factory)
