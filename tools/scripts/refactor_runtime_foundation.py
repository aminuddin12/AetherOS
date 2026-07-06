import os

files = {
    "runtime/src/aether_runtime/context/context.py": """
from dataclasses import dataclass, field
from typing import Dict, Any, Optional
import uuid

@dataclass(frozen=True)
class RuntimeContext:
    user_id: str = "system"
    workspace_id: Optional[str] = None
    locale: str = "en-US"
    correlation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    permissions: tuple = field(default_factory=tuple)
    metadata: tuple = field(default_factory=tuple)  # Workaround for frozen Dict/List

    def copy_with(self, **kwargs):
        from dataclasses import replace
        return replace(self, **kwargs)
""",
    "runtime/src/aether_runtime/session/session.py": """
from enum import Enum
from ..context.context import RuntimeContext
from typing import Optional

class SessionState(Enum):
    CREATED = "Created"
    OPENING = "Opening"
    OPENED = "Opened"
    BUSY = "Busy"
    IDLE = "Idle"
    CLOSING = "Closing"
    CLOSED = "Closed"
    DISPOSED = "Disposed"

class RuntimeSession:
    def __init__(self, context: RuntimeContext):
        self._context = context
        self.state = SessionState.CREATED

    @property
    def context(self) -> RuntimeContext:
        return self._context

    async def start(self):
        self.state = SessionState.OPENING
        # perform opening logic
        self.state = SessionState.OPENED
        self.state = SessionState.IDLE

    async def stop(self):
        self.state = SessionState.CLOSING
        # perform closing logic
        self.state = SessionState.CLOSED
        self.state = SessionState.DISPOSED
""",
    "runtime/src/aether_runtime/middleware/pipeline.py": """
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
""",
    "runtime/src/aether_runtime/events/dispatcher.py": """
from typing import Callable, Dict, List

class RuntimeEventDispatcher:
    def __init__(self):
        self.listeners: Dict[str, List[Callable]] = {}

    def subscribe(self, event_name: str, callback: Callable):
        if event_name not in self.listeners:
            self.listeners[event_name] = []
        self.listeners[event_name].append(callback)

    async def dispatch(self, event_name: str, **kwargs):
        for callback in self.listeners.get(event_name, []):
            await callback(**kwargs)

    async def translate_and_dispatch(self, kernel_event: str, **kwargs):
        # Translate Kernel event to Runtime event
        event_map = {
            "KernelWorkerStarted": "RuntimeExecutionStarted",
            "KernelReady": "RuntimeReady"
        }
        runtime_event = event_map.get(kernel_event, kernel_event)
        await self.dispatch(runtime_event, **kwargs)

event_dispatcher = RuntimeEventDispatcher()
"""
}

for path, content in files.items():
    with open(path, "w") as f:
        f.write(content.strip() + "\n")

print("✅ Phase 2 foundations completed.")
