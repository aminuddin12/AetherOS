from typing import List, Dict, Any
import time
from .base import RuntimeDescriptor, RuntimeState, RuntimeContext
from .health import LifecycleState, HealthState
from .registry import RuntimeRegistry
from .graph import RuntimeGraph
from .manager import RuntimeManager
from .resolution import CapabilityResolver, CapabilityDescriptor

class BootstrapError(Exception):
    pass

class BootstrapEngine:
    def __init__(
        self,
        registry: RuntimeRegistry,
        resolver: CapabilityResolver,
        manager: RuntimeManager,
        graph: RuntimeGraph
    ) -> None:
        self._registry = registry
        self._resolver = resolver
        self._manager = manager
        self._graph = graph

    def bootstrap(
        self,
        descriptors: List[RuntimeDescriptor],
        capabilities: List[CapabilityDescriptor],
        instances: Dict[str, Any],
        context: RuntimeContext
    ) -> None:
        for cap in capabilities:
            self._resolver.register_capability_descriptor(cap)
            
        for desc in descriptors:
            state = RuntimeState(
                lifecycle_state=LifecycleState.CREATED,
                health_state=HealthState.HEALTHY
            )
            self._registry.register_runtime(desc, state)
            self._graph.add_node(desc.runtime_id)
            
            for dep in desc.requires:
                try:
                    cap_desc = self._resolver.resolve_capability(dep)
                    self._graph.add_dependency(desc.runtime_id, cap_desc.provider)
                except Exception as e:
                    raise BootstrapError(f"Failed resolving requirement: {dep} for {desc.runtime_id}") from e

        ordered_runtimes = self._graph.validate_and_sort()
        
        for runtime_id in ordered_runtimes:
            desc = self._registry.get_descriptor(runtime_id)
            state = self._registry.get_state(runtime_id)
            if not desc or not state:
                raise BootstrapError(f"Missing registry entry for sorted node: {runtime_id}")
                
            state.lifecycle_state = LifecycleState.DISCOVERED
            state.lifecycle_state = LifecycleState.REGISTERED
            state.lifecycle_state = LifecycleState.RESOLVED
            
            instance = instances.get(runtime_id)
            if not instance:
                raise BootstrapError(f"Concrete instance missing for: {runtime_id}")
                
            self._manager.host_runtime(runtime_id, instance)
            state.lifecycle_state = LifecycleState.INITIALIZED
            state.initialized_at = time.time()
            
            state.lifecycle_state = LifecycleState.STARTING
            state.lifecycle_state = LifecycleState.RUNNING
            state.started_at = time.time()
            
            state.lifecycle_state = LifecycleState.READY
