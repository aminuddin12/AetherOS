from pydantic import Field
from ..base import ValueObject


class Branch(ValueObject):
    """
    Representasi cabang (branch) VCS.
    """

    repository_id: str = Field(..., description="The repository")
    name: str = Field(..., description="Branch name (e.g., 'feature/auth')")
    head_commit: str = Field(..., description="Latest commit SHA")
