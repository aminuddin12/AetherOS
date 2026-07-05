from pydantic import Field
from ..base import ValueObject

class CostRecord(ValueObject):
    """
    Pencatatan biaya finansial dalam sistem.
    """
    currency: str = Field(default="USD", description="ISO 4217 currency code")
    amount: float = Field(..., description="Total cost amount")
    billable_entity_id: str = Field(..., description="ID of the workspace or project billed")
