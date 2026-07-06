from abc import ABC, abstractmethod
from typing import Any, List

class ExecutionStrategy(ABC):
    """
    Menentukan BAGAIMANA sekelompok unit kerja dieksekusi.
    Contoh: Sequential, Parallel, Batch, MapReduce.
    """

    @abstractmethod
    async def execute(self, units: List[Any], executor_fn: Any) -> List[Any]:
        """Menjalankan units menggunakan executor_fn sesuai strategi."""
        ...
