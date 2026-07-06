from enum import StrEnum
from pydantic import Field
from ..base import Entity


class CredentialType(StrEnum):
    PASSWORD = "password"
    API_KEY = "api_key"
    OAUTH_TOKEN = "oauth_token"
    CERTIFICATE = "certificate"


class Credential(Entity):
    """
    Representasi dari rahasia atau token yang membuktikan identitas.
    Hanya mendefinisikan referensi, BUKAN nilai secret plaintext.
    """

    identity_id: str = Field(..., description="Owner of the credential")
    credential_type: CredentialType = Field(..., description="Type of authentication secret")
    is_active: bool = Field(default=True, description="Whether this credential is valid")
