from pydantic import Field
from ..base import Entity

class ArchitecturePattern(Entity):
    """
    Pola arsitektur atau kode sukses yang dapat direplikasi.
    """
    name: str = Field(..., description="Pattern name (e.g., 'CQRS in Laravel')")
    context_applied: str = Field(..., description="When to use this pattern")
    example_implementation: str = Field(..., description="Code snippet or structural example")
