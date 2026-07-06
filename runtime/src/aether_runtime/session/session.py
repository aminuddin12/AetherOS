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
