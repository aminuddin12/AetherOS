# AetherOS Executor Integration Tests
# Integration tests for Executor SPI with execution engine

import pytest
import time
import asyncio
from core.execution.engine import ExecutionEngine
from core.execution.executor_pool.pool import ExecutorPool, PoolType
from core.execution.execution_context.context import ExecutionContext
from core.execution.execution_result.result import ExecutionStatus


def test_execution_engine_with_executor_spi():
    """Test execution engine integration with Executor SPI."""
    engine = ExecutionEngine()
    engine.initialize()

    descriptor = engine.get_descriptor()
    assert descriptor.name == "aetheros-engine"
    assert len(descriptor.available_executors) == 1
    assert "default-thread-pool" in [e.name for e in descriptor.available_executors]


def test_executor_pool_registration():
    """Test custom executor pool registration."""
    engine = ExecutionEngine()
    engine.initialize()

    custom_pool = ExecutorPool(
        pool_type=PoolType.THREAD,
        max_workers=4,
        name="custom-pool"
    )
    custom_pool.initialize()

    engine.register_executor("custom-pool", custom_pool)

    descriptor = engine.get_descriptor()
    assert len(descriptor.available_executors) == 2
    assert "custom-pool" in [e.name for e in descriptor.available_executors]


def test_task_execution_with_different_executors():
    """Test task execution with different executor types."""
    engine = ExecutionEngine()
    engine.initialize()

    def test_task(x, y):
        return x ** y

    thread_result = engine.execute_task(test_task, 2, 3, executor_id="default-thread-pool")
    assert thread_result == 8

    custom_pool = ExecutorPool(pool_type=PoolType.THREAD, max_workers=2, name="custom-pool")
    custom_pool.initialize()
    engine.register_executor("custom-pool", custom_pool)
    custom_result = engine.execute_task(test_task, 3, 2, executor_id="custom-pool")
    assert custom_result == 9


def test_async_execution():
    """Test asynchronous execution."""
    engine = ExecutionEngine()
    engine.initialize()

    def long_running_task(seconds):
        time.sleep(seconds)
        return f"Completed after {seconds} seconds"

    async_result = engine.execute_async(long_running_task, 0.1, executor_id="default-thread-pool")
    assert async_result.status == ExecutionStatus.PENDING

    result = async_result.output.result()
    assert result == "Completed after 0.1 seconds"


def test_executor_health_monitoring():
    """Test executor health monitoring."""
    engine = ExecutionEngine()
    engine.initialize()

    executor = engine.get_executor("default-thread-pool")
    health = executor.health()
    assert health.healthy
    assert health.message == "OK"
    assert health.details['status'] == "INITIALIZED"


def test_engine_shutdown():
    """Test engine shutdown with executors."""
    engine = ExecutionEngine()
    engine.initialize()

    def test_task():
        return "test"

    result = engine.execute_task(test_task)
    assert result == "test"

    engine.shutdown()
    executor = engine.get_executor("default-thread-pool")
    assert executor.get_status().name == "STOPPED"