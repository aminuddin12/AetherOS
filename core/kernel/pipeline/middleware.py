from typing import Protocol, Any, Callable, Awaitable

NextMiddleware = Callable[[Any], Awaitable[Any]]

class PipelineMiddleware(Protocol):
    async def invoke(self, context: Any, next_mid: NextMiddleware) -> Any: ...
