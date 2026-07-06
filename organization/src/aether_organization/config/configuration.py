from pydantic import BaseModel
from typing import Dict, Any, Optional

class SecretsReference(BaseModel):
    provider_uri: str
    key: str

class OrganizationConfiguration(BaseModel):
    defaults: Dict[str, Any]
    overrides: Dict[str, Any]
    environment: str
    secrets_references: Dict[str, SecretsReference]

class OrganizationCapabilities(BaseModel):
    compute_allowlist: list[str]
    model_allowlist: list[str]
    storage_limit_gb: int
    memory_limit_mb: int
    network_egress_allowed: bool
    experimental_flags: Dict[str, bool]
