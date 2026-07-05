from pydantic import Field
from typing import Dict
from .value_object import ValueObject

class ResourceReference(ValueObject):
    """
    Pointers ke resource lain untuk mencegah deep object graph.
    Sangat cocok untuk Event Sourcing dan penyimpanan relasional.
    """
    id: str = Field(..., description="Unique ID of the referenced resource")
    kind: str = Field(..., description="Type of the resource (e.g., 'Worker', 'Task')")
    namespace: str = Field(default="default", description="Resource namespace")
    name: str | None = Field(default=None, description="Human readable name")
    version: str | None = Field(default=None, description="Specific version if applicable")
    labels: Dict[str, str] = Field(default_factory=dict, description="Cached labels for fast filtering")
