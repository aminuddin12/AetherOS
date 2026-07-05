from typing import Dict, Type, TypeVar, Any
from .scope import ServiceScope
from .provider import ServiceProvider
from .resolver import Resolver

T = TypeVar('T')

class ServiceContainer:
    """
    Pure Python IoC Container.
    Mendukung Singleton dan Transient. Constructor Injection otomatis via Type Hints.
    """
    def __init__(self):
        self._providers: Dict[Type, ServiceProvider] = {}
        self._resolver = Resolver(self)
        
        # Self registration
        self.register_instance(ServiceContainer, self)

    def register(self, interface: Type[T], implementation: Type[T] | None = None, scope: ServiceScope = ServiceScope.SINGLETON) -> None:
        impl = implementation or interface
        self._providers[interface] = ServiceProvider(impl, scope)

    def register_instance(self, interface: Type[T], instance: T) -> None:
        provider = ServiceProvider(lambda: instance, ServiceScope.SINGLETON)
        provider.instance = instance
        self._providers[interface] = provider

    def resolve(self, interface: Type[T]) -> T:
        provider = self._providers.get(interface)
        if not provider:
            # Attempt to auto-resolve if concrete class
            return self._resolver.build(interface)
        return provider.get(self._resolver)
