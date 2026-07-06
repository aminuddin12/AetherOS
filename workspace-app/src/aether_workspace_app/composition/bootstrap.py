from .registry import DefaultRegistry
from aether_runtime.sdk import AetherRuntime
from typing import Any

class ApplicationBootstrap:
    """Composition root for assembling runtime dependencies."""
    
    @staticmethod
    def wire_dependencies(runtime: AetherRuntime) -> DefaultRegistry:
        registry = DefaultRegistry()
        # Wire facades from runtime SDK
        registry.register("storage", runtime.storage)
        registry.register("repository", runtime.repository)
        registry.register("artifact", runtime.artifact)
        registry.register("workspace", runtime.workspace)
        return registry
