from .retry_policy import RetryPolicy
from .timeout_policy import TimeoutPolicy


class ExecutionPolicy:
    """
    Menggabungkan seluruh policy yang mengatur eksekusi.
    """

    def __init__(
        self,
        retry: RetryPolicy | None = None,
        timeout: TimeoutPolicy | None = None,
    ):
        self.retry = retry or RetryPolicy()
        self.timeout = timeout or TimeoutPolicy()
