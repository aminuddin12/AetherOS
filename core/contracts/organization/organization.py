from pydantic import Field
from ..base import AggregateRoot

class Organization(AggregateRoot):
    """
    Entitas teratas (Root Tenant).
    """
    name: str = Field(..., description="Company name (e.g., 'AetherOS Inc')")
    domain: str = Field(..., description="Company primary domain")
    is_active: bool = Field(default=True)
