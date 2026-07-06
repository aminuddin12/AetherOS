from abc import ABC, abstractmethod
from typing import Any, Dict, List


class ExecutorCapability:
    def __init__(self, name: str, version: str = "1.0"):
        self.name = name
        self.version = version


class ExecutorHealth:
    def __init__(self, healthy: bool = True, message: str = "OK"):
        self.healthy = healthy
        self.message = message


class Executor(ABC):
    """
    Universal Executor Interface.
    Semua jenis executor (AI, Docker, Human, SSH, CLI, Browser, MCP)
    harus mengimplementasikan interface ini.
    """

    @abstractmethod
    async def execute(self, context: "ExecutionContext", payload: Any) -> Any:
        """Menjalankan payload dalam context yang diberikan."""
        ...

    @abstractmethod
    async def validate(self, context: "ExecutionContext", payload: Any) -> bool:
        """Memvalidasi apakah executor dapat menjalankan payload ini."""
        ...

    @abstractmethod
    async def cancel(self) -> None:
        """Membatalkan eksekusi yang sedang berjalan."""
        ...

    @abstractmethod
    async def shutdown(self) -> None:
        """Membersihkan resource dan mematikan executor."""
        ...

    @abstractmethod
    def health(self) -> ExecutorHealth:
        """Melaporkan status kesehatan executor."""
        ...

    @abstractmethod
    def capabilities(self) -> List[ExecutorCapability]:
        """Mendeklarasikan kemampuan executor."""
        ...
