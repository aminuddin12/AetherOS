# AetherOS Executor SPI (ADR-0007)
# Universal Service Provider Interface for execution capabilities

from abc import ABC, abstractmethod
from typing import Any, Callable, Optional, Union, List, Protocol
from enum import Enum, auto
from dataclasses import dataclass
from core.execution.cancellation.token import CancellationToken
from core.execution.metrics.collector import MetricsCollector
from core.execution.execution_result.result import ExecutionResult
from core.execution.execution_context.context import ExecutionContext


class ExecutorType(Enum):
    """Type of executor implementation."""
    SYNCHRONOUS = auto()
    ASYNCHRONOUS = auto()
    THREAD_POOL = auto()
    PROCESS_POOL = auto()
    DISTRIBUTED = auto()


class ExecutorStatus(Enum):
    """Current status of an executor."""
    CREATED = auto()
    INITIALIZED = auto()
    RUNNING = auto()
    PAUSED = auto()
    STOPPED = auto()
    FAILED = auto()


@dataclass
class ExecutorCapability:
    """Metadata describing an executor capability."""
    name: str
    version: str = "1.0"
    description: str = ""


@dataclass
class ExecutorHealth:
    """Health status of an executor."""
    healthy: bool = True
    message: str = "OK"
    details: dict = None


@dataclass
class ExecutorDescriptor:
    """Metadata describing an executor implementation."""
    name: str
    executor_type: ExecutorType
    description: str
    version: str
    capabilities: List[ExecutorCapability]
    supported_strategies: List[str]


class Executor(Protocol):
    """Universal Executor Service Provider Interface (SPI).
    
    All executor types (AI, Docker, Human, SSH, CLI, Browser, MCP)
    must implement this interface.
    """

    @abstractmethod
    def initialize(self, context: Optional[ExecutionContext] = None) -> None:
        """Initialize the executor with optional execution context."""
        pass

    @abstractmethod
    def execute(self, 
                task: Callable[..., Any],
                *args: Any,
                **kwargs: Any) -> Union[ExecutionResult, Any]:
        """Execute a callable task with provided arguments.
        
        Args:
            task: Callable to execute
            *args: Positional arguments for the task
            **kwargs: Keyword arguments for the task
            
        Returns:
            ExecutionResult or direct result depending on executor type
        """
        pass

    @abstractmethod
    async def execute_async(self, 
                     task: Callable[..., Any],
                     *args: Any,
                     **kwargs: Any) -> ExecutionResult:
        """Execute a callable task asynchronously.
        
        Args:
            task: Callable to execute
            *args: Positional arguments for the task
            **kwargs: Keyword arguments for the task
            
        Returns:
            ExecutionResult with future or promise
        """
        pass

    @abstractmethod
    def cancel(self, token: CancellationToken) -> bool:
        """Cancel ongoing execution using cancellation token.
        
        Args:
            token: CancellationToken for the execution
            
        Returns:
            True if cancellation was successful, False otherwise
        """
        pass

    @abstractmethod
    def get_status(self) -> ExecutorStatus:
        """Get current status of the executor.
        
        Returns:
            Current ExecutorStatus
        """
        pass

    @abstractmethod
    def get_descriptor(self) -> ExecutorDescriptor:
        """Get executor descriptor with metadata.
        
        Returns:
            ExecutorDescriptor with metadata
        """
        pass

    @abstractmethod
    def set_metrics_collector(self, collector: MetricsCollector) -> None:
        """Set metrics collector for the executor.
        
        Args:
            collector: MetricsCollector instance
        """
        pass

    @abstractmethod
    def health(self) -> ExecutorHealth:
        """Get health status of the executor.
        
        Returns:
            ExecutorHealth status
        """
        pass

    @abstractmethod
    def capabilities(self) -> List[ExecutorCapability]:
        """Get list of capabilities supported by this executor.
        
        Returns:
            List of ExecutorCapability objects
        """
        pass

    @abstractmethod
    def shutdown(self) -> None:
        """Cleanup and shutdown the executor."""
        pass
        """Mendeklarasikan kemampuan executor."""
        ...
