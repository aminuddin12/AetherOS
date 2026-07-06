from typing import Any, List
from core.execution.spi import ExecutionStrategy


class SequentialStrategy(ExecutionStrategy):
    """Menjalankan units satu per satu secara berurutan."""

    async def execute(self, units: List[Any], executor_fn: Any) -> List[Any]:
        results = []
        for unit in units:
            result = await executor_fn(unit)
            results.append(result)
        return results
