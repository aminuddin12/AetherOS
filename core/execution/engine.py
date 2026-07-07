# AetherOS Execution Engine
# Core execution engine implementation (ADR-0006)

from typing import Dict, List, Optional, Callable, Any, Union
from enum import Enum
from dataclasses import dataclass
from core.execution.spi.executor import Executor, ExecutorDescriptor, ExecutorStatus
from core.execution.executor_pool.pool import ExecutorPool, PoolType
from core.execution.execution_context.context import ExecutionContext
from core.execution.execution_result.result import ExecutionResult
from core.execution.execution_plan.plan import ExecutionPlan
from core.execution.execution_strategy.registry import ExecutionStrategyRegistry
from core.execution.metrics.collector import MetricsCollector
from core.execution.cancellation.token import CancellationToken
from core.execution.internal.exceptions import ExecutionError


class EngineStatus(Enum):
    """Execution engine status."""
    CREATED = "created"
    INITIALIZED = "initialized"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"
    FAILED = "failed"


@dataclass
class EngineDescriptor:
    """Metadata describing the execution engine."""
    name: str
    version: str
    description: str
    supported_strategies: List[str]
    available_executors: List[ExecutorDescriptor]


class ExecutionEngine:
    """Core execution engine for AetherOS."""

    def __init__(self, name: str = "aetheros-engine"):
        """Initialize execution engine."""
        self.name = name
        self.status = EngineStatus.CREATED
        self._executors: Dict[str, Executor] = {}
        self._strategy_registry = ExecutionStrategyRegistry()
        self._metrics_collector = MetricsCollector()
        self._default_pool = None
        self._context = None

    def initialize(self, context: Optional[ExecutionContext] = None) -> None:
        """Initialize the execution engine."""
        if self.status != EngineStatus.CREATED:
            return
            
        try:
            self._context = context or ExecutionContext()
            
            # Create default executor pools
            self._default_pool = ExecutorPool(
                pool_type=PoolType.THREAD,
                name="default-thread-pool"
            )
            self._default_pool.initialize(self._context)
            self.register_executor("default-thread-pool", self._default_pool)
            
            # Register process pool
            process_pool = ExecutorPool(
                pool_type=PoolType.PROCESS,
                name="default-process-pool"
            )
            process_pool.initialize(self._context)
            self.register_executor("default-process-pool", process_pool)
            
            self.status = EngineStatus.INITIALIZED
            
        except Exception as e:
            self.status = EngineStatus.FAILED
            raise ExecutionError(f"Engine initialization failed: {e}")

    def register_executor(self, executor_id: str, executor: Executor) -> None:
        """Register an executor with the engine."""
        executor.initialize(self._context)
        executor.set_metrics_collector(self._metrics_collector)
        self._executors[executor_id] = executor

    def get_executor(self, executor_id: str) -> Executor:
        """Get an executor by ID."""
        return self._executors.get(executor_id)

    def list_executors(self) -> List[ExecutorDescriptor]:
        """List all available executors."""
        return [executor.get_descriptor() for executor in self._executors.values()]

    def execute(self, 
                plan: ExecutionPlan,
                strategy: str = "sequential",
                executor_id: str = "default-thread-pool") -> ExecutionResult:
        """Execute an execution plan."""
        if self.status != EngineStatus.INITIALIZED:
            self.initialize()
            
        try:
            executor = self._executors.get(executor_id)
            if not executor:
                raise ExecutionError(f"Executor '{executor_id}' not found")
                
            strategy_impl = self._strategy_registry.get_strategy(strategy)
            if not strategy_impl:
                raise ExecutionError(f"Strategy '{strategy}' not found")
                
            self.status = EngineStatus.RUNNING
            result = strategy_impl.execute(plan, executor, self._context)
            self.status = EngineStatus.INITIALIZED
            
            return result
            
        except Exception as e:
            self.status = EngineStatus.FAILED
            raise ExecutionError(f"Execution failed: {e}")

    def execute_task(self, 
                    task: Callable[..., Any],
                    *args: Any,
                    executor_id: str = "default-thread-pool",
                    **kwargs: Any) -> Union[ExecutionResult, Any]:
        """Execute a single task."""
        executor = self._executors.get(executor_id)
        if not executor:
            raise ExecutionError(f"Executor '{executor_id}' not found")
            
        return executor.execute(task, *args, **kwargs)

    def execute_async(self, 
                     task: Callable[..., Any],
                     *args: Any,
                     executor_id: str = "default-thread-pool",
                     **kwargs: Any) -> ExecutionResult:
        """Execute a task asynchronously."""
        executor = self._executors.get(executor_id)
        if not executor:
            raise ExecutionError(f"Executor '{executor_id}' not found")
            
        return executor.execute_async(task, *args, **kwargs)

    def cancel(self, token: CancellationToken) -> bool:
        """Cancel ongoing execution."""
        success = True
        for executor in self._executors.values():
            if not executor.cancel(token):
                success = False
        return success

    def get_descriptor(self) -> EngineDescriptor:
        """Get engine descriptor."""
        return EngineDescriptor(
            name=self.name,
            version="1.0",
            description="AetherOS Execution Engine",
            supported_strategies=self._strategy_registry.list_strategies(),
            available_executors=self.list_executors()
        )

    def shutdown(self) -> None:
        """Shutdown the engine and all executors."""
        for executor in self._executors.values():
            executor.shutdown()
        self.status = EngineStatus.STOPPED