class ExecutionError(Exception):
    """Base exception for execution-related errors."""
    pass


class ExecutorError(ExecutionError):
    """Base exception for executor-related errors."""
    pass


class ExecutionEngineError(ExecutionError):
    """Root exception for Execution Engine."""
    pass


class ExecutorNotFoundError(ExecutorError):
    """Executor not found."""
    pass


class ExecutorAllocationError(ExecutorError):
    """Failed to allocate executor from pool."""
    pass


class ExecutionTimeoutError(ExecutionError):
    """Execution exceeded time limit."""
    pass


class ExecutionCancelledError(ExecutionError):
    """Execution was cancelled."""
    pass


class TaskValidationError(ExecutionError):
    """Task validation failed."""
    pass


class ExecutionRetryExhaustedError(ExecutionEngineError):
    """Semua percobaan retry telah habis."""

    pass


class ExecutionValidationError(ExecutionEngineError):
    """Payload gagal validasi sebelum eksekusi."""

    pass
