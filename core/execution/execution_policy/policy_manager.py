from core.execution.spi import ExecutionPolicy, RetryPolicy, TimeoutPolicy


class ExecutionPolicyManager:
    """
    Menyimpan dan meresolve policy berdasarkan konteks eksekusi.
    """

    def __init__(self, default_policy: ExecutionPolicy | None = None):
        self._default = default_policy or ExecutionPolicy()

    def get_policy(self, task_id: str | None = None) -> ExecutionPolicy:
        return self._default
