from .token import CancellationToken


class CancellationTokenSource:
    """
    Sumber yang mengontrol CancellationToken.
    Hanya pemilik source yang boleh memicu cancel.
    """

    def __init__(self):
        self._token = CancellationToken()

    @property
    def token(self) -> CancellationToken:
        return self._token

    def cancel(self, reason: str = "Cancellation requested") -> None:
        self._token._reason = reason
        self._token._event.set()
