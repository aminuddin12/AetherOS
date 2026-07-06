from enum import StrEnum
from pydantic import Field
from ..base import Entity


class EnvironmentType(StrEnum):
    LOCAL = "local"
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class Environment(Entity):
    """
    Definisi env (Mis: AWS Staging, K8s Prod).
    """

    name: str = Field(..., description="Environment name")
    type: EnvironmentType = Field(..., description="Env level")
    is_protected: bool = Field(
        default=False, description="Whether it requires HITL approval to deploy"
    )
