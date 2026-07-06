from typing import Optional
from datetime import datetime, timedelta
import asyncio

class WorkspaceLease:
    def __init__(self, owner: str, duration: int):
        self.owner = owner
        self.expires_at = datetime.utcnow() + timedelta(seconds=duration)

    @property
    def is_expired(self) -> bool:
        return datetime.utcnow() > self.expires_at

class AdvancedLockManager:
    def __init__(self):
        self._lock = asyncio.Lock()
        self.active_lease: Optional[WorkspaceLease] = None

    async def acquire(self, owner: str, ttl: int = 60) -> bool:
        await self._lock.acquire()
        try:
            if self.active_lease and not self.active_lease.is_expired:
                return False
            self.active_lease = WorkspaceLease(owner, ttl)
            return True
        finally:
            self._lock.release()

    async def release(self, owner: str) -> bool:
        await self._lock.acquire()
        try:
            if self.active_lease and self.active_lease.owner == owner:
                self.active_lease = None
                return True
            return False
        finally:
            self._lock.release()
