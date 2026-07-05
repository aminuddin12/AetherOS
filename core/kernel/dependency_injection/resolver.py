import inspect
from typing import Any, Callable, Dict, Type
from .exceptions import DependencyResolutionError

class Resolver:
    def __init__(self, container: 'ServiceContainer'):
        self.container = container

    def build(self, factory: Callable[..., Any]) -> Any:
        sig = inspect.signature(factory)
        kwargs = {}
        for name, param in sig.parameters.items():
            if param.annotation == inspect.Parameter.empty:
                raise DependencyResolutionError(f"Missing type hint for '{name}' in '{factory.__name__}'")
            try:
                kwargs[name] = self.container.resolve(param.annotation)
            except Exception as e:
                if param.default != inspect.Parameter.empty:
                    kwargs[name] = param.default
                else:
                    raise DependencyResolutionError(f"Cannot resolve '{name}' for '{factory.__name__}': {str(e)}")
        return factory(**kwargs)
