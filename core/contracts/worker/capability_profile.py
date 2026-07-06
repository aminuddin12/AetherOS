from typing import List
from enum import StrEnum
from pydantic import Field
from ..base import ValueObject, Entity


class ProficiencyLevel(StrEnum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class Capability(Entity):
    """
    Kemampuan/Skill absolut yang immutable (mis: 'Python', 'Vue3').
    """

    name: str = Field(..., description="Skill name")
    category: str = Field(default="general", description="Skill category")


class CapabilityRecord(ValueObject):
    """
    Rekaman penguasaan suatu skill oleh agent tertentu (Mutable state).
    """

    skill: Capability = Field(..., description="The immutable skill")
    level: ProficiencyLevel = Field(default=ProficiencyLevel.BEGINNER)
    confidence: float = Field(default=0.5, description="Confidence score (0.0 to 1.0)")
    version: str | None = Field(
        default=None, description="Specific tool/skill version (e.g. '3.12')"
    )


class CapabilityProfile(ValueObject):
    """
    Kumpulan rekaman kemampuan agen.
    """

    records: List[CapabilityRecord] = Field(default_factory=list)
