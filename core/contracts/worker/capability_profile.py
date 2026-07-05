from typing import List
from pydantic import Field
from ..base import ValueObject

class Capability(ValueObject):
    """
    Kemampuan spesifik yang dikuasai agen (mis: 'Python', 'Vue3', 'PostgreSQL').
    """
    name: str = Field(..., description="Skill or tool name")
    proficiency: float = Field(default=1.0, description="Proficiency level (0.0 to 1.0)")

class CapabilityProfile(ValueObject):
    """
    Kumpulan kemampuan agen yang membedakannya dengan agen lain.
    """
    capabilities: List[Capability] = Field(default_factory=list)
