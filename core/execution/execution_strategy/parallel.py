import asyncio
from typing import Any, List
from core.execution.spi import ExecutionStrategy

class ParallelStrategy(ExecutionStrategy):
    """Menjalankan semua units secara paralel menggunakan asyncio.gather."""

    async def execute(self, units: List[Any], executor_fn: Any) -> List[Any]:
        tasks = [executor_fn(unit) for unit in units]
        return list(await asyncio.gather(*tasks, return_exceptions=True))
