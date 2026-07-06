from typing import List
from pydantic import Field
from ..base import AggregateRoot
from .environment import Environment


class Workspace(AggregateRoot):
    """
    Area kerja terisolasi (sandbox policy bound) tempat agen beroperasi.
    """

    project_id: str = Field(..., description="Project this workspace belongs to")
    name: str = Field(..., description="Workspace name (e.g., 'ERP Backend Dev')")
    environments: List[Environment] = Field(default_factory=list)
