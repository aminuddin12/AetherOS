from enum import StrEnum
from pydantic import Field
from ..base import ValueObject
from .identity import Identity

class PrincipalType(StrEnum):
    USER = "user"
    AGENT = "agent"
    SYSTEM = "system"

class Principal(ValueObject):
    """
    Aktor yang sedang mengeksekusi aksi dalam konteks aktif.
    """
    identity_id: str = Field(..., description="ID of the underlying Identity")
    type: PrincipalType = Field(..., description="Type of the principal")
    name: str = Field(..., description="Human readable name of the principal")
