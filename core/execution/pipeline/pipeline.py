from typing import List, Any
from core.execution.spi import ExecutionMiddleware


class ExecutionPipeline:
    """
    Middleware-based execution pipeline.
    Merangkai middleware secara berurutan dengan pola chain-of-responsibility.
    """

    def __init__(self):
        self._middlewares: List[ExecutionMiddleware] = []

    def use(self, middleware: ExecutionMiddleware) -> "ExecutionPipeline":
        self._middlewares.append(middleware)
        return self

    async def execute(self, context: Any, payload: Any) -> Any:
        async def terminal(ctx: Any, pl: Any) -> Any:
            return pl

        chain = terminal
        for mw in reversed(self._middlewares):
            current_mw = mw
            previous_chain = chain

            async def make_next(ctx: Any, pl: Any, _mw=current_mw, _prev=previous_chain) -> Any:
                return await _mw.invoke(ctx, pl, _prev)

            chain = make_next

        return await chain(context, payload)
