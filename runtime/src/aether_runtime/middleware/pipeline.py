from typing import Callable, Any, List
from ..session.session import RuntimeSession
from ..events.dispatcher import event_dispatcher

class Middleware:
    async def process(self, session: RuntimeSession, action_name: str, next_func: Callable) -> Any:
        return await next_func()

class MiddlewarePipeline:
    def __init__(self):
        self.middlewares: List[Middleware] = []

    def use(self, middleware: Middleware):
        self.middlewares.append(middleware)

    async def execute(self, session: RuntimeSession, action_name: str, func: Callable, *args, **kwargs) -> Any:
        await event_dispatcher.dispatch("CommandExecuted", action=action_name, correlation_id=session.context.correlation_id)
        
        async def _run_next(index: int) -> Any:
            if index < len(self.middlewares):
                return await self.middlewares[index].process(session, action_name, lambda: _run_next(index + 1))
            else:
                return await func(*args, **kwargs)
        
        try:
            return await _run_next(0)
        except Exception as e:
            await event_dispatcher.dispatch("CommandFailed", action=action_name, error=str(e))
            raise e
