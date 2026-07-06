from typing import Dict

class ResourceManager:
    """
    In-memory resource manager untuk mengatur slot eksekusi.
    """
    def __init__(self, max_concurrent: int = 10):
        self._max = max_concurrent
        self._allocated: Dict[str, bool] = {}

    @property
    def available_slots(self) -> int:
        return self._max - len(self._allocated)

    def acquire(self, session_id: str) -> bool:
        if self.available_slots <= 0:
            return False
        self._allocated[session_id] = True
        return True

    def release(self, session_id: str) -> None:
        self._allocated.pop(session_id, None)
