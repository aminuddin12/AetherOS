class RetryPolicy:
    """
    Aturan retry untuk eksekusi yang gagal.
    """
    def __init__(
        self,
        max_retries: int = 3,
        delay_seconds: float = 1.0,
        backoff_multiplier: float = 2.0,
        retryable_exceptions: tuple = (Exception,),
    ):
        self.max_retries = max_retries
        self.delay_seconds = delay_seconds
        self.backoff_multiplier = backoff_multiplier
        self.retryable_exceptions = retryable_exceptions

    def should_retry(self, attempt: int, error: Exception) -> bool:
        if attempt >= self.max_retries:
            return False
        return isinstance(error, self.retryable_exceptions)

    def get_delay(self, attempt: int) -> float:
        return self.delay_seconds * (self.backoff_multiplier ** attempt)
