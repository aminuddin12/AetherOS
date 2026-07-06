from dataclasses import dataclass
from typing import Dict
from .provider import StorageProvider

@dataclass
class MountPoint:
    path: str
    provider: StorageProvider
    options: dict

class MountManager:
    """Manages virtual mount points across the storage subsystem."""
    def __init__(self):
        self._mounts: Dict[str, MountPoint] = {}

    def mount(self, path: str, provider: StorageProvider, **options) -> None:
        self._mounts[path] = MountPoint(path, provider, options)

    def unmount(self, path: str) -> None:
        if path in self._mounts:
            del self._mounts[path]
