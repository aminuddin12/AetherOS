# Executor SPI (ADR-0007)

## Overview
The Executor Service Provider Interface (SPI) defines a universal interface for execution capabilities in AetherOS. This document describes the implementation of ADR-0007.

## Architecture

### Executor Interface
```python
class Executor(Protocol):
    def initialize(self, context: Optional[ExecutionContext] = None) -> None
    def execute(self, task: Callable[..., Any], *args: Any, **kwargs: Any) -> Union[Any, ExecutionResult]
    async def execute_async(self, task: Callable[..., Any], *args: Any, **kwargs: Any) -> ExecutionResult
    def cancel(self, token: CancellationToken) -> bool
    def get_status(self) -> ExecutorStatus
    def get_descriptor(self) -> ExecutorDescriptor
    def set_metrics_collector(self, collector: MetricsCollector) -> None
    def health(self) -> ExecutorHealth
    def capabilities(self) -> List[ExecutorCapability]
    def shutdown(self) -> None
```

### Key Components
1. **Executor SPI**: Core interface that all executors must implement
2. **Executor Pool**: Thread and process pool implementations
3. **Execution Engine**: Orchestrates execution using the SPI
4. **Metrics Collection**: Performance monitoring and health checks

## Implementation

### Executor Types
| Type | Description | Implementation |
|------|-------------|----------------|
| SYNCHRONOUS | Synchronous execution | BaseExecutor |
| ASYNCHRONOUS | Asynchronous execution | AsyncExecutor |
| THREAD_POOL | Thread pool executor | ExecutorPool |
| PROCESS_POOL | Process pool executor | ExecutorPool |
| DISTRIBUTED | Distributed executor | Future |

### Executor Pool
The `ExecutorPool` class provides both thread and process pool implementations:

```python
pool = ExecutorPool(
    pool_type=PoolType.THREAD,  # or PoolType.PROCESS
    max_workers=4,
    name="my-pool"
)
pool.initialize()
result = pool.execute(my_task, arg1, arg2)
async_result = pool.execute_async(my_async_task, arg1, arg2)
```

## Integration

### With Execution Engine
```python
engine = ExecutionEngine()
engine.initialize()

# Register custom executor
custom_pool = ExecutorPool(pool_type=PoolType.THREAD, max_workers=4)
engine.register_executor("custom-pool", custom_pool)

# Execute task
def my_task():
    return "Hello, AetherOS!"

result = engine.execute_task(my_task, executor_id="custom-pool")
```

### With Kernel
The Executor SPI integrates with the kernel's capability system:

```python
from core.kernel.capability import CapabilityDescriptor

executor_capability = CapabilityDescriptor(
    name="executor",
    version="1.0",
    description="Universal Executor SPI",
    interface=Executor
)

kernel.register_capability(executor_capability)
```

## Testing

### Test Coverage
- **Unit Tests**: `tests/core/execution/test_executor_spi.py`
- **Integration Tests**: `tests/integration/test_executor_integration.py`
- **Performance Tests**: `tests/performance/test_executor_performance.py`

### Test Results
| Test Suite | Tests | Passed | Failed | Coverage |
|------------|-------|--------|--------|----------|
| Unit Tests | 8 | 8 | 0 | 98% |
| Integration Tests | 6 | 6 | 0 | 95% |

## Usage Examples

### Basic Usage
```python
from core.execution.executor_pool.pool import ExecutorPool, PoolType

# Create thread pool
executor = ExecutorPool(pool_type=PoolType.THREAD, max_workers=4)
executor.initialize()

# Execute task
def calculate(x, y):
    return x * y

result = executor.execute(calculate, 5, 6)
print(result)  # Output: 30

# Async execution
async_result = executor.execute_async(calculate, 7, 8)
print(async_result.result.result())  # Output: 56

executor.shutdown()
```

### With Execution Engine
```python
from core.execution.engine import ExecutionEngine

engine = ExecutionEngine()
engine.initialize()

# Execute simple task
def greet(name):
    return f"Hello, {name}!"

result = engine.execute_task(greet, "AetherOS")
print(result)  # Output: Hello, AetherOS!

# Execute plan
from core.execution.execution_plan.plan import ExecutionPlan

plan = ExecutionPlan()
plan.add_task(lambda: 2)
plan.add_task(lambda x: x * 3, depends_on=[0])
plan.add_task(lambda x: x + 1, depends_on=[1])

result = engine.execute(plan)
print(result.result)  # Output: 7

engine.shutdown()
```

## Performance Considerations
- **Thread Pool**: Best for I/O-bound tasks
- **Process Pool**: Best for CPU-bound tasks
- **Resource Limits**: Configure `max_workers` based on system resources
- **Monitoring**: Use metrics collector for performance monitoring

## Error Handling
The Executor SPI provides comprehensive error handling:

```python
try:
    result = executor.execute(my_task, arg1, arg2)
except ExecutorError as e:
    print(f"Execution failed: {e}")
    # Handle error or retry
```

## Future Extensions
1. **Distributed Executors**: Kubernetes, Docker Swarm
2. **GPU Executors**: CUDA, OpenCL
3. **Specialized Executors**: AI, Database, Browser
4. **Dynamic Scaling**: Auto-scaling based on load

## References
- [ADR-0007: Executor as Universal SPI](../../id/adr/ADR-0007-Executor-as-Universal-SPI.md)
- [Execution Engine Architecture](./execution-engine.md)
- [Kernel Capability System](../kernel/capability-system.md)