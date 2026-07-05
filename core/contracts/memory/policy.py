from pydantic import Field
from ..base import Entity

class OrganizationalPolicy(Entity):
    """
    Aturan (Constitution) yang disintesis untuk membatasi perilaku agen.
    """
    domain: str = Field(..., description="E.g., 'security', 'coding_standard'")
    rule_statement: str = Field(..., description="The exact rule agents must follow")
    is_enforced: bool = Field(default=True, description="Whether Kernel actively enforces this")
