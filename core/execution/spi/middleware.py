from abc import ABC, abstractmethod
from typing import Any, Callable, Awaitable

NextMiddleware = Callable[["ExecutionContext", Any], Awaitable[Any]]


class ExecutionMiddleware(ABC):
    """
    Middleware untuk Execution Pipeline.
    Setiap middleware dapat memproses, memodifikasi, atau menolak eksekusi
    sebelum meneruskannya ke middleware berikutnya.
    """

    @abstractmethod
    async def invoke(self, context: Any, payload: Any, next_mw: NextMiddleware) -> Any:
        """Memproses dan meneruskan ke middleware berikutnya."""
        ...
