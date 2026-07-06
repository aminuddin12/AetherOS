from ..core.session import WorkspaceSession, WorkspaceHealth
from .events import event_bus, WorkspaceEventType
import asyncio

class WorkspaceLockManager:
    def __init__(self):
        self._lock = asyncio.Lock()
        self._owner = None

    async def acquire(self, owner: str):
        await self._lock.acquire()
        self._owner = owner

    def release(self, owner: str):
        if self._owner == owner:
            self._owner = None
            self._lock.release()

    @property
    def is_locked(self) -> bool:
        return self._lock.locked()

class WorkspaceCoordinator:
    def __init__(self):
        self.lock_manager = WorkspaceLockManager()

    async def open_workspace(self, session: WorkspaceSession):
        session.open()
        await event_bus.emit(WorkspaceEventType.OPENED, workspace_id=session.context.workspace_id)

    async def close_workspace(self, session: WorkspaceSession):
        session.close()
        await event_bus.emit(WorkspaceEventType.CLOSED, workspace_id=session.context.workspace_id)

    async def lock_workspace(self, session: WorkspaceSession, reason: str):
        await self.lock_manager.acquire(session.context.user_id if hasattr(session.context, 'user_id') else "system")
        session.health = WorkspaceHealth.LOCKED
        await event_bus.emit(WorkspaceEventType.LOCKED, workspace_id=session.context.workspace_id, reason=reason)

    def unlock_workspace(self, session: WorkspaceSession):
        self.lock_manager.release(session.context.user_id if hasattr(session.context, 'user_id') else "system")
        session.health = WorkspaceHealth.HEALTHY
        # Note: can't await inside sync method, would need an async wrapper in real implementation
