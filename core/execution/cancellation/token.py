import asyncio


class CancellationToken:
    """
    Token cooperative cancellation (read-only view).
    Executor memeriksa token ini secara periodik.
    """

    def __init__(self):
        self._event = asyncio.Event()
        self._reason: str = ""

    @property
    def is_cancelled(self) -> bool:
        return self._event.is_set()

    @property
    def reason(self) -> str:
        return self._reason

    async def wait_for_cancellation(self) -> None:
        await self._event.wait()
