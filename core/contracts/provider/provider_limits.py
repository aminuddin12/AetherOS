from pydantic import Field
from ..base import ValueObject


class ProviderLimits(ValueObject):
    """
    Batas operasional (Quotas & Context Window).
    """

    max_context_tokens: int = Field(..., description="Maximum context window")
    max_output_tokens: int = Field(..., description="Maximum output window")
    rate_limit_requests_per_minute: int = Field(default=60)
    rate_limit_tokens_per_minute: int = Field(default=100000)
