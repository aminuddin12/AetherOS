from typing import Callable, Any
from .buses.bus import Command

class MiddlewarePipeline:
    def __init__(self):
        self.middlewares = []

    def use(self, middleware: Callable):
        self.middlewares.append(middleware)

    async def execute(self, command: Command, handler: Callable) -> Any:
        # Simplistic pipeline execution
        async def run_pipeline(idx: int, cmd: Command) -> Any:
            if idx < len(self.middlewares):
                return await self.middlewares[idx](cmd, lambda c: run_pipeline(idx + 1, c))
            return await handler(cmd)
            
        return await run_pipeline(0, command)
