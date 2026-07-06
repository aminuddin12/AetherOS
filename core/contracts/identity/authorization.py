from typing import List
from pydantic import Field
from ..base import ValueObject


class PermissionRecord(ValueObject):
    """
    Representasi izin akses ke sebuah sumber daya.
    """

    resource: str = Field(..., description="Target resource (e.g., 'workspace.file')")
    action: str = Field(..., description="Action allowed (e.g., 'read', 'write')")
    effect: str = Field(default="allow", description="'allow' or 'deny'")


class RoleRecord(ValueObject):
    """
    Kumpulan permission yang dikelompokkan dalam peran (Role).
    """

    name: str = Field(..., description="Role name")
    permissions: List[PermissionRecord] = Field(
        default_factory=list, description="Associated permissions"
    )
