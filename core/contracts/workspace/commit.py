from pydantic import Field
from ..base import ValueObject

class Commit(ValueObject):
    """
    Perubahan atomik (VCS commit).
    """
    repository_id: str = Field(..., description="The repository")
    sha: str = Field(..., description="Commit hash")
    message: str = Field(..., description="Commit message")
    author_identity_id: str = Field(..., description="Who authored it")
