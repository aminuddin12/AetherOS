from ..application.buses.bus import CommandBus, QueryBus
from ..application.pipeline.engine import MiddlewarePipeline

class ApplicationEngine:
    """Core orchestrator executing commands/queries through pipeline."""
    def __init__(self, registry):
        self.registry = registry
        self.pipeline = MiddlewarePipeline()
        self.command_bus = CommandBus(registry)
        self.query_bus = QueryBus(registry)
        
    async def execute_command(self, command) -> any:
        # Simplistic pipeline integration
        handler = self.registry.get(f"{type(command).__name__}Handler")
        if not handler:
            raise ValueError(f"No handler registered for {type(command).__name__}")
        return await self.pipeline.execute(command, handler.handle)

    async def execute_query(self, query) -> any:
        return await self.query_bus.query(query)
