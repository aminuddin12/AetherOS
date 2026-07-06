from typing import Dict, Any
from pydantic import BaseModel, ConfigDict, Field


class BaseContract(BaseModel):
    """
    Fondasi paling bawah untuk semua model AetherOS (API Public).
    Menyediakan versioning dan Kubernetes-style metadata.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    # Versioning
    schema_version: str = Field(default="1.0", description="Schema version of this contract")
    contract_version: str = Field(default="1.0", description="Data contract compatibility version")
    api_version: str = Field(default="v1", description="API route version")
    spec_version: str = Field(default="1.0", description="Specification/Behavioral version")

    # Metadata
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Generic metadata")
    labels: Dict[str, str] = Field(
        default_factory=dict, description="Identifying labels (e.g., tier: backend)"
    )
    annotations: Dict[str, str] = Field(
        default_factory=dict, description="Non-identifying metadata"
    )
    tags: list[str] = Field(default_factory=list, description="Categorization tags")
    extensions: Dict[str, Any] = Field(
        default_factory=dict, description="Plugin specific extensions"
    )

    # Ownership
    owner: str | None = Field(default=None, description="Resource owner reference")
    created_by: str | None = Field(default=None, description="Who created this resource")
    managed_by: str = Field(
        default="aether-kernel", description="Controller managing this resource"
    )
