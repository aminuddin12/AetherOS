# AetherOS Executor Pool
# Thread and process pool implementation for Executor SPI (ADR-0007)

import concurrent.futures
import multiprocessing
import threading
from typing import Dict, List, Optional, Union, Callable, Any
from dataclasses import dataclass, field
from enum import Enum
from core.execution.spi.executor import (
    Executor, ExecutorType, ExecutorStatus, 
    ExecutorDescriptor, ExecutorCapability, ExecutorHealth
)
from core.execution.cancellation.token import CancellationToken
from core.execution.metrics.collector import MetricsCollector
from core.execution.execution_result.result import ExecutionResult, ExecutionStatus
from core.execution.execution_context.context import ExecutionContext
from core.execution.internal.exceptions import ExecutorError, ExecutorNotFoundError, ExecutorAllocationError


class PoolType(Enum):
    """Type of executor pool."""
    THREAD = "thread"
    PROCESS = "process"


@dataclass
class PoolMetrics:
    """Metrics for executor pool."""
    active_tasks: int = 0
    completed_tasks: int = 0
    failed_tasks: int = 0
    queue_size: int = 0
    pool_size: int = 0
    utilization: float = 0.0


class BaseExecutorPool:
    """
    Base pool manager for Executor instances.
    """

    def __init__(self):
        self._executors: Dict[str, Executor] = {}
        self._allocated: Dict[str, str] = {}
        self._lock = threading.RLock()

    def register(self, executor_id: str, executor: Executor) -> None:
        """Register an executor with the pool."""
        with self._lock:
            self._executors[executor_id] = executor

    def unregister(self, executor_id: str) -> None:
        """Unregister an executor from the pool."""
        with self._lock:
            self._executors.pop(executor_id, None)
            self._allocated = {k: v for k, v in self._allocated.items() if v != executor_id}

    def lookup(self, executor_id: str) -> Executor:
        """Lookup an executor by ID."""
        with self._lock:
            executor = self._executors.get(executor_id)
            if not executor:
                raise ExecutorNotFoundError(f"Executor '{executor_id}' not found in pool")
            return executor

    def allocate(self, session_id: str, executor_id: str | None = None) -> Executor:
        """Allocate an executor for a session."""
        with self._lock:
            if executor_id:
                executor = self.lookup(executor_id)
                self._allocated[session_id] = executor_id
                return executor
            for eid, ex in self._executors.items():
                if eid not in self._allocated.values():
                    self._allocated[session_id] = eid
                    return ex
            raise ExecutorAllocationError("No available executors in pool")

    def release(self, session_id: str) -> None:
        """Release an executor from a session."""
        with self._lock:
            self._allocated.pop(session_id, None)

    def list_available(self) -> List[str]:
        """List available executor IDs."""
        with self._lock:
            allocated_ids = set(self._allocated.values())
            return [eid for eid in self._executors if eid not in allocated_ids]


class ExecutorPool(Executor, BaseExecutorPool):
    """Executor pool implementation supporting thread and process pools."""

    def __init__(self, 
                 pool_type: PoolType = PoolType.THREAD,
                 max_workers: Optional[int] = None,
                 name: str = "executor-pool"):
        """
        Initialize executor pool.
        
        Args:
            pool_type: Type of pool (THREAD or PROCESS)
            max_workers: Maximum number of workers (default: CPU count)
            name: Name of the pool
        """
        BaseExecutorPool.__init__(self)
        self.pool_type = pool_type
        self.max_workers = max_workers or multiprocessing.cpu_count()
        self.name = name
        self._pool = None
        self._status = ExecutorStatus.CREATED
        self._metrics = PoolMetrics()
        self._metrics_collector = None

    def initialize(self, context: Optional[ExecutionContext] = None) -> None:
        """Initialize the executor pool."""
        with self._lock:
            if self._status != ExecutorStatus.CREATED:
                return

            try:
                if self.pool_type == PoolType.THREAD:
                    self._pool = concurrent.futures.ThreadPoolExecutor(
                        max_workers=self.max_workers,
                        thread_name_prefix=f"{self.name}-thread"
                    )
                else:
                    self._pool = concurrent.futures.ProcessPoolExecutor(
                        max_workers=self.max_workers,
                        initializer=self._process_initializer
                    )
                
                self._status = ExecutorStatus.INITIALIZED
                self._update_metrics()
                
            except Exception as e:
                self._status = ExecutorStatus.FAILED
                raise ExecutorError(f"Failed to initialize pool: {e}")

    def _process_initializer(self):
        """Initializer for process pool workers."""
        # Set process-specific configurations here
        pass

    def execute(self, 
                task: Callable[..., Any],
                *args: Any,
                **kwargs: Any) -> Union[ExecutionResult, Any]:
        """Execute a task synchronously."""
        if self._status != ExecutorStatus.INITIALIZED:
            self.initialize()
            
        try:
            future = self._pool.submit(task, *args, **kwargs)
            result = future.result()
            self._update_metrics()
            return result
        except Exception as e:
            self._metrics.failed_tasks += 1
            self._update_metrics()
            raise ExecutorError(f"Execution failed: {e}")

    async def execute_async(self, 
                     task: Callable[..., Any],
                     *args: Any,
                     **kwargs: Any) -> ExecutionResult:
        """Execute a task asynchronously."""
        if self._status != ExecutorStatus.INITIALIZED:
            self.initialize()
            
        try:
            future = self._pool.submit(task, *args, **kwargs)
            result = ExecutionResult(
                output=future,
                status=ExecutionStatus.PENDING,
            )
            self._metrics.active_tasks += 1
            self._update_metrics()
            
            # Add callback for completion
            future.add_done_callback(self._task_completed)
            return result
        except Exception as e:
            self._metrics.failed_tasks += 1
            self._update_metrics()
            raise ExecutorError(f"Async execution failed: {e}")

    def _task_completed(self, future: concurrent.futures.Future):
        """Callback when task completes."""
        with self._lock:
            self._metrics.active_tasks -= 1
            if future.exception():
                self._metrics.failed_tasks += 1
            else:
                self._metrics.completed_tasks += 1
            self._update_metrics()

    def cancel(self, token: CancellationToken) -> bool:
        """Cancel ongoing execution."""
        # Note: concurrent.futures doesn't support direct cancellation
        # This is a placeholder for future implementation
        return False

    def get_status(self) -> ExecutorStatus:
        """Get current status."""
        return self._status

    def get_descriptor(self) -> ExecutorDescriptor:
        """Get executor descriptor."""
        return ExecutorDescriptor(
            name=self.name,
            executor_type=ExecutorType.THREAD_POOL if self.pool_type == PoolType.THREAD 
                        else ExecutorType.PROCESS_POOL,
            description=f"{self.pool_type.value} pool with {self.max_workers} workers",
            version="1.0",
            capabilities=[
                ExecutorCapability(
                    name="parallel_execution",
                    description="Supports parallel task execution"
                ),
                ExecutorCapability(
                    name="async_execution",
                    description="Supports asynchronous execution"
                )
            ],
            supported_strategies=["parallel", "sequential"]
        )

    def set_metrics_collector(self, collector: MetricsCollector) -> None:
        """Set metrics collector."""
        self._metrics_collector = collector

    def health(self) -> ExecutorHealth:
        """Get health status."""
        if self._status == ExecutorStatus.FAILED:
            return ExecutorHealth(
                healthy=False,
                message="Executor pool failed",
                details={"status": self._status.name}
            )
        
        return ExecutorHealth(
            healthy=True,
            message="OK",
            details={
                "status": self._status.name,
                "pool_type": self.pool_type.value,
                "max_workers": self.max_workers,
                **self._metrics.__dict__
            }
        )

    def capabilities(self) -> List[ExecutorCapability]:
        """Get capabilities."""
        return self.get_descriptor().capabilities

    def _update_metrics(self):
        """Update pool metrics."""
        if self._pool:
            with self._lock:
                self._metrics.pool_size = self.max_workers
                self._metrics.utilization = (
                    self._metrics.active_tasks / self.max_workers
                    if self.max_workers > 0 else 0.0
                )
                
                if self._metrics_collector:
                    self._metrics_collector.collect("executor_pool", self._metrics)

    def shutdown(self) -> None:
        """Shutdown the pool."""
        if self._pool:
            self._pool.shutdown(wait=True)
            self._status = ExecutorStatus.STOPPED
            self._update_metrics()
