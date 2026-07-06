from pydantic import BaseModel

class RepositoryReference(BaseModel):
    """Reference to a specific repository."""
    uri: str

class RevisionReference(BaseModel):
    """Reference to a specific revision."""
    repository_uri: str
    revision_id: str

class BranchReference(BaseModel):
    """Reference to a specific branch."""
    repository_uri: str
    branch_name: str

class CommitReference(BaseModel):
    """Reference to a specific commit."""
    repository_uri: str
    commit_id: str

class TagReference(BaseModel):
    """Reference to a specific tag."""
    repository_uri: str
    tag_name: str
