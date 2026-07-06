from pydantic import Field
from ..base import ValueObject


class ProviderCapability(ValueObject):
    """
    Fitur spesifik yang didukung oleh model/provider.
    """

    supports_vision: bool = Field(default=False)
    supports_function_calling: bool = Field(default=False)
    supports_structured_outputs: bool = Field(default=False)
    supports_streaming: bool = Field(default=False)
