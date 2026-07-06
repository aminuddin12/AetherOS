from typing import List
from pydantic import BaseModel, Field
from .health import HealthModel


class DiagnosticsReport(BaseModel):
    version: str = Field(...)
    health: HealthModel = Field(...)
    loaded_services: List[str] = Field(default_factory=list)
    loaded_extensions: List[str] = Field(default_factory=list)
    loaded_registries: List[str] = Field(default_factory=list)
