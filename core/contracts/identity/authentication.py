from enum import StrEnum
from pydantic import Field
from datetime import datetime
from ..base import ValueObject
from .principal import Principal

class AuthenticationState(StrEnum):
    AUTHENTICATED = "authenticated"
    ANONYMOUS = "anonymous"
    EXPIRED = "expired"

class AuthenticationContext(ValueObject):
    """
    Konteks hasil otentikasi saat ini.
    """
    state: AuthenticationState = Field(..., description="Current state of authentication")
    principal: Principal | None = Field(default=None, description="The authenticated principal")
    authenticated_at: datetime | None = Field(default=None, description="When the authentication occurred")
    expires_at: datetime | None = Field(default=None, description="When the session expires")
