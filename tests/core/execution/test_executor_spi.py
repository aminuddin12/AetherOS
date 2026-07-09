# AetherOS Executor SPI Tests
# Tests for Executor SPI implementation (ADR-0007)

import pytest
import time
import threading
from typing import Any, Callable
from core.execution.spi.executor import (
    Executor, ExecutorType, ExecutorStatus, 
    ExecutorDescriptor, ExecutorCapability, ExecutorHealth
)
from core.execution.executor_pool.pool import ExecutorPool, PoolType
from core.execution.cancellation.token import CancellationToken
from core.execution.metrics.collector import MetricsCollector
from core.execution.execution_result.result import ExecutionResult, ExecutionStatus
from core.execution.execution_context.context import ExecutionContext
from core.execution.internal.exceptions import ExecutorError


class MockExecutor(Executor):
    """Mock executor for testing."""

    def __init__(self, name: str = "mock-executor"):
        self.name = name
        self.status = ExecutorStatus.CREATED
        self.metrics_collector = None
        self.initialize_called = False
        self.execute_called = False
        self.execute_async_called = False
        self.cancel_called = False
        self.shutdown_called = False

    def initialize(self, context: ExecutionContext = None) -> None:
        self.initialize_called = True
        self.status = ExecutorStatus.INITIALIZED

    def execute(self, task: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        self.execute_called = True
        return task(*args, **kwargs)

    async def execute_async(self, task: Callable[..., Any], *args: Any, **kwargs: Any) -> ExecutionResult:
        self.execute_async_called = True
        result = task(*args, **kwargs)
        return ExecutionResult(
            output=result,
            status=ExecutionStatus.SUCCESS,
        )

    def cancel(self, token: CancellationToken) -> bool:
        self.cancel_called = True
        return True

    def get_status(self) -> ExecutorStatus:
        return self.status

    def get_descriptor(self) -> ExecutorDescriptor:
        return ExecutorDescriptor(
            name=self.name,
            executor_type=ExecutorType.SYNCHRONOUS,
            description="Mock executor for testing",
            version="1.0",
            capabilities=[ExecutorCapability("mock")],
            supported_strategies=["sequential"]
        )

    def set_metrics_collector(self, collector: MetricsCollector) -> None:
        self.metrics_collector = collector

    def health(self) -> ExecutorHealth:
        return ExecutorHealth(healthy=True, message="OK")

    def capabilities(self):
        return [ExecutorCapability("mock")]

    def shutdown(self) -> None:
        self.shutdown_called = True
        self.status = ExecutorStatus.STOPPED


def test_executor_spi_interface():
    """Test that the Executor SPI interface is properly defined."""
    executor = MockExecutor()
    
    # Test interface methods exist
    assert hasattr(executor, 'initialize')
    assert hasattr(executor, 'execute')
    assert hasattr(executor, 'execute_async')
    assert hasattr(executor, 'cancel')
    assert hasattr(executor, 'get_status')
    assert hasattr(executor, 'get_descriptor')
    assert hasattr(executor, 'set_metrics_collector')
    assert hasattr(executor, 'health')
    assert hasattr(executor, 'capabilities')
    assert hasattr(executor, 'shutdown')


def test_executor_lifecycle():
    """Test executor lifecycle methods."""
    executor = MockExecutor()
    context = ExecutionContext()
    
    # Test initialization
    executor.initialize(context)
    assert executor.initialize_called
    assert executor.get_status() == ExecutorStatus.INITIALIZED
    
    # Test descriptor
    descriptor = executor.get_descriptor()
    assert descriptor.name == "mock-executor"
    assert descriptor.executor_type == ExecutorType.SYNCHRONOUS
    assert len(descriptor.capabilities) == 1
    
    # Test health
    health = executor.health()
    assert health.healthy
    assert health.message == "OK"
    
    # Test shutdown
    executor.shutdown()
    assert executor.shutdown_called
    assert executor.get_status() == ExecutorStatus.STOPPED


def test_executor_execution():
    """Test executor execution methods."""
    import asyncio
    executor = MockExecutor()
    executor.initialize()
    
    # Test synchronous execution
    def test_task(x, y):
        return x + y
    
    result = executor.execute(test_task, 2, 3)
    assert result == 5
    assert executor.execute_called
    
    # Test asynchronous execution
    async_result = asyncio.run(executor.execute_async(test_task, 4, 5))
    assert async_result.status == ExecutionStatus.SUCCESS
    assert async_result.output == 9
    assert executor.execute_async_called


def test_executor_pool_initialization():
    """Test executor pool initialization."""
    pool = ExecutorPool(pool_type=PoolType.THREAD, max_workers=2, name="test-pool")
    assert pool.get_status() == ExecutorStatus.CREATED
    
    pool.initialize()
    assert pool.get_status() == ExecutorStatus.INITIALIZED
    
    descriptor = pool.get_descriptor()
    assert descriptor.name == "test-pool"
    assert descriptor.executor_type == ExecutorType.THREAD_POOL
    assert len(descriptor.capabilities) == 2


def test_executor_pool_execution():
    """Test executor pool task execution."""
    pool = ExecutorPool(pool_type=PoolType.THREAD, max_workers=2, name="test-pool")
    pool.initialize()
    
    def test_task(x, y):
        return x * y
    
    # Test synchronous execution
    result = pool.execute(test_task, 3, 4)
    assert result == 12
    
    # Test asynchronous execution
    import asyncio
    async_result = asyncio.run(pool.execute_async(test_task, 5, 6))
    assert async_result.status == ExecutionStatus.PENDING
    
    # Wait for completion
    time.sleep(0.1)
    assert async_result.output.result() == 30


def test_executor_pool_metrics():
    """Test executor pool metrics collection."""
    collector = MetricsCollector()
    pool = ExecutorPool(pool_type=PoolType.THREAD, max_workers=2, name="test-pool")
    pool.set_metrics_collector(collector)
    pool.initialize()
    
    def test_task():
        time.sleep(0.05)
        return "done"
    
    # Execute multiple tasks
    for _ in range(3):
        pool.execute(test_task)
    
    # Check metrics
    health = pool.health()
    assert health.healthy
    assert health.details['active_tasks'] >= 0
    assert health.details['completed_tasks'] >= 0
    assert health.details['pool_size'] == 2


def test_executor_pool_shutdown():
    """Test executor pool shutdown."""
    pool = ExecutorPool(pool_type=PoolType.THREAD, max_workers=2, name="test-pool")
    pool.initialize()
    
    pool.shutdown()
    assert pool.get_status() == ExecutorStatus.STOPPED
    
    # Test health after shutdown
    health = pool.health()
    assert health.healthy
    assert health.details['status'] == "STOPPED"