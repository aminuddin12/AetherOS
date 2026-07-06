from typing import Any, Dict
from pydantic import Field
from uuid import UUID
from ..base import ValueObject


class SystemResponse(ValueObject):
    """
    Hasil balasan dari SystemCommand atau SystemQuery.
    """

    correlation_id: UUID = Field(..., description="ID of the original Command or Query")
    success: bool = Field(..., description="Whether the operation was successful")
    data: Any = Field(default=None, description="Response payload")
    errors: Dict[str, str] = Field(
        default_factory=dict, description="Error details if success=False"
    )
