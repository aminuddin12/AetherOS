from typing import Any, Protocol, runtime_checkable

@runtime_checkable
class Command(Protocol):
    pass

@runtime_checkable
class CommandHandler(Protocol):
    async def handle(self, command: Command) -> Any: ...

class CommandBus:
    def __init__(self, registry):
        self.registry = registry

    async def execute(self, command: Command) -> Any:
        handler = self.registry.get(f"{type(command).__name__}Handler")
        if not handler:
            raise ValueError(f"No handler registered for {type(command).__name__}")
        # Simplistic bus, doesn't route through pipeline yet
        return await handler.handle(command)

@runtime_checkable
class Query(Protocol):
    pass

@runtime_checkable
class QueryHandler(Protocol):
    async def handle(self, query: Query) -> Any: ...

class QueryBus:
    def __init__(self, registry):
        self.registry = registry

    async def query(self, query: Query) -> Any:
        handler = self.registry.get(f"{type(query).__name__}Handler")
        if not handler:
            raise ValueError(f"No handler registered for {type(query).__name__}")
        return await handler.handle(query)
