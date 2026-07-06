class TimeoutPolicy:
    """
    Aturan timeout untuk eksekusi.
    """
    def __init__(
        self,
        execution_timeout_seconds: float = 300.0,
        session_timeout_seconds: float = 3600.0,
    ):
        self.execution_timeout_seconds = execution_timeout_seconds
        self.session_timeout_seconds = session_timeout_seconds
