from typing import Dict, List, Any
from .base import RuntimeDescriptor, RuntimeState

class RuntimeRegistry:
    def __init__(self) -> None:
        self._descriptors: Dict[str, RuntimeDescriptor] = {}
        self._states: Dict[str, RuntimeState] = {}

    def register_runtime(self, descriptor: RuntimeDescriptor, state: RuntimeState) -> None:
        self._descriptors[descriptor.runtime_id] = descriptor
        self._states[descriptor.runtime_id] = state

    def get_descriptor(self, runtime_id: str) -> RuntimeDescriptor | None:
        return self._descriptors.get(runtime_id)

    def get_state(self, runtime_id: str) -> RuntimeState | None:
        return self._states.get(runtime_id)

    def list_runtimes(self) -> List[str]:
        return list(self._descriptors.keys())

class CapabilityRegistry:
    def __init__(self) -> None:
        self._capabilities: Dict[str, str] = {}

    def register_capability(self, capability_id: str, provider_runtime_id: str) -> None:
        self._capabilities[capability_id] = provider_runtime_id

    def get_provider(self, capability_id: str) -> str | None:
        return self._capabilities.get(capability_id)

class ServiceRegistry:
    def __init__(self) -> None:
        self._services: Dict[str, Any] = {}

    def register_service(self, service_id: str, endpoint: Any) -> None:
        self._services[service_id] = endpoint

    def get_service(self, service_id: str) -> Any | None:
        return self._services.get(service_id)

class ExtensionRegistry:
    def __init__(self) -> None:
        self._extensions: List[Any] = []

    def register_extension(self, extension: Any) -> None:
        self._extensions.append(extension)

    def list_extensions(self) -> List[Any]:
        return self._extensions

class EventRegistry:
    def __init__(self) -> None:
        self._handlers: Dict[str, List[Any]] = {}

    def subscribe(self, event_type: str, handler: Any) -> None:
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    def get_handlers(self, event_type: str) -> List[Any]:
        return self._handlers.get(event_type, [])
