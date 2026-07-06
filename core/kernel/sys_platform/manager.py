from typing import Dict, Any

class RuntimeManagerError(Exception):
    pass

class RuntimeManager:
    def __init__(self) -> None:
        self._instances: Dict[str, Any] = {}

    def host_runtime(self, runtime_id: str, instance: Any) -> None:
        self._instances[runtime_id] = instance

    def get_runtime(self, runtime_id: str) -> Any:
        instance = self._instances.get(runtime_id)
        if not instance:
            raise RuntimeManagerError(f"Runtime instance not found for: {runtime_id}")
        return instance

    def release_runtime(self, runtime_id: str) -> None:
        self._instances.pop(runtime_id, None)
