class ExecutionEngineError(Exception):
    """Root exception untuk Execution Engine."""
    pass

class ExecutorNotFoundError(ExecutionEngineError):
    """Tidak ada executor yang cocok ditemukan."""
    pass

class ExecutorAllocationError(ExecutionEngineError):
    """Gagal mengalokasikan executor dari pool."""
    pass

class ExecutionTimeoutError(ExecutionEngineError):
    """Eksekusi melebihi batas waktu."""
    pass

class ExecutionCancelledError(ExecutionEngineError):
    """Eksekusi dibatalkan."""
    pass

class ExecutionRetryExhaustedError(ExecutionEngineError):
    """Semua percobaan retry telah habis."""
    pass

class ExecutionValidationError(ExecutionEngineError):
    """Payload gagal validasi sebelum eksekusi."""
    pass
