from typing import List
from pydantic import Field
from ..base import Entity
from .tool import Tool


class Skill(Entity):
    """
    Makro atau workflow kompleks yang merangkai beberapa Tools sekaligus.
    """

    name: str = Field(..., description="Skill name (e.g., 'DeployToAWS')")
    description: str = Field(..., description="What this skill accomplishes")
    required_tools: List[Tool] = Field(default_factory=list, description="Underlying tools used")
