from pydantic import Field
from ..base import ValueObject


class ProviderPricing(ValueObject):
    """
    Skema tarif per token/request (dalam USD).
    """

    cost_per_1k_input_tokens: float = Field(default=0.0)
    cost_per_1k_output_tokens: float = Field(default=0.0)
