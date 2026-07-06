from typing import Dict
from core.execution.spi import ExecutionStrategy

class StrategyRegistry:
    """Registry untuk mendaftarkan dan menemukan strategy berdasarkan nama."""

    def __init__(self):
        self._strategies: Dict[str, ExecutionStrategy] = {}

    def register(self, name: str, strategy: ExecutionStrategy) -> None:
        self._strategies[name] = strategy

    def get(self, name: str) -> ExecutionStrategy | None:
        return self._strategies.get(name)
