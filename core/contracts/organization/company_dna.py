from typing import List
from pydantic import Field
from ..base import Entity


class CompanyDNA(Entity):
    """
    Budaya, filosofi, dan prinsip utama organisasi.
    Bagian inti dari Company Brain yang dipelajari setiap agen baru.
    """

    organization_id: str = Field(..., description="Owning organization")
    core_values: List[str] = Field(default_factory=list, description="Guiding principles")
    communication_style: str = Field(..., description="E.g., 'Professional, direct, no jargon'")
