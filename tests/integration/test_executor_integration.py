# AetherOS Executor Integration Tests
# Integration tests for Executor SPI with execution engine

import pytest
import time
from core.execution.engine import ExecutionEngine
from core.execution.executor_pool.pool import ExecutorPool, PoolType
from core.execution.execution_plan.plan import ExecutionPlan
from core.execution.execution_context.context import ExecutionContext
from core.execution.execution_result.result import ExecutionResult


def test_execution_engine_with_executor_spi():
    """Test execution engine integration with Executor SPI."""
    engine = ExecutionEngine()
    engine.initialize()
    
    # Test engine descriptor
    descriptor = engine.get_descriptor()
    assert descriptor.name == "aetheros-engine"
    assert len(descriptor.available_executors) == 2
    assert "default-thread-pool" in [e.name for e in descriptor.available_executors]
    assert "default-process-pool" in [e.name for e in descriptor.available_executors]


def test_executor_pool_registration():
    """Test custom executor pool registration."""
    engine = ExecutionEngine()
    engine.initialize()
    
    # Create and register custom pool
    custom_pool = ExecutorPool(
        pool_type=PoolType.THREAD,
        max_workers=4,
        name="custom-pool"
    )
    custom_pool.initialize()
    
    engine.register_executor("custom-pool", custom_pool)
    
    # Verify registration
    descriptor = engine.get_descriptor()
    assert len(descriptor.available_executors) == 3
    assert "custom-pool" in [e.name for e in descriptor.available_executors]


def test_task_execution_with_different_executors():
    """Test task execution with different executor types."""
    engine = ExecutionEngine()
    engine.initialize()
    
    def test_task(x, y):
        return x ** y
    
    # Test with thread pool
    thread_result = engine.execute_task(test_task, 2, 3, executor_id="default-thread-pool")
    assert thread_result == 8
    
    # Test with process pool
    process_result = engine.execute_task(test_task, 3, 2, executor_id="default-process-pool")
    assert process_result == 9


def test_async_execution():
    """Test asynchronous execution."""
    engine = ExecutionEngine()
    engine.initialize()
    
    def long_running_task(seconds):
        time.sleep(seconds)
        return f"Completed after {seconds} seconds"
    
    # Start async execution
    async_result = engine.execute_async(long_running_task, 0.1, executor_id="default-thread-pool")
    assert async_result.status == "PENDING"
    
    # Wait for completion
    result = async_result.result.result()
    assert result == "Completed after 0.1 seconds"


def test_execution_plan_with_executor():
    """Test execution plan with executor integration."""
    engine = ExecutionEngine()
    engine.initialize()
    
    # Create execution plan
    def task1():
        return "task1"
    
    def task2(result):
        return f"{result} -> task2"
    
    plan = ExecutionPlan()
    plan.add_task(task1)
    plan.add_task(task2, depends_on=[0])
    
    # Execute plan
    result = engine.execute(plan, strategy="sequential", executor_id="default-thread-pool")
    assert result.status == "COMPLETED"
    assert result.result == "task1 -> task2"


def test_executor_health_monitoring():
    """Test executor health monitoring."""
    engine = ExecutionEngine()
    engine.initialize()
    
    # Check health of all executors
    for executor_id in ["default-thread-pool", "default-process-pool"]:
        executor = engine.get_executor(executor_id)
        health = executor.health()
        assert health.healthy
        assert health.message == "OK"
        assert health.details['status'] == "INITIALIZED"


def test_engine_shutdown():
    """Test engine shutdown with executors."""
    engine = ExecutionEngine()
    engine.initialize()
    
    # Execute a task
    def test_task():
        return "test"
    
    result = engine.execute_task(test_task)
    assert result == "test"
    
    # Shutdown engine
    engine.shutdown()
    
    # Verify all executors are stopped
    for executor_id in ["default-thread-pool", "default-process-pool"]:
        executor = engine.get_executor(executor_id)
        assert executor.get_status() == ExecutorStatus.STOPPED