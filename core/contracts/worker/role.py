from pydantic import Field
from ..base import Entity


class Role(Entity):
    """
    Definisi persona agen (mis: 'Senior Backend Developer', 'QA Tester').
    """

    title: str = Field(..., description="Job title")
    description: str = Field(..., description="Role responsibilities")
    system_prompt_template: str = Field(..., description="Base system prompt for LLM")
