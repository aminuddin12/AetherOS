from typing import Protocol, runtime_checkable, List
from ..core.domain import Commit, Diff, History
from ..references.models import RepositoryReference, RevisionReference

@runtime_checkable
class RepositoryBackend(Protocol):
    """Agnostic abstraction for version control operations."""
    
    async def initialize(self, uri: str) -> RepositoryReference:
        ...
        
    async def clone(self, source_uri: str, target_uri: str) -> RepositoryReference:
        ...
        
    async def fetch(self, repo: RepositoryReference) -> None:
        ...
        
    async def push(self, repo: RepositoryReference) -> None:
        ...
        
    async def pull(self, repo: RepositoryReference) -> None:
        ...
        
    async def checkout(self, revision: RevisionReference) -> None:
        ...
        
    async def commit(self, repo: RepositoryReference, message: str, tree_uri: str) -> Commit:
        ...
        
    async def merge(self, source: RevisionReference, target: RevisionReference) -> Commit:
        ...
        
    async def diff(self, base: RevisionReference, target: RevisionReference) -> Diff:
        ...
        
    async def history(self, revision: RevisionReference) -> History:
        ...
        
    async def references(self, repo: RepositoryReference) -> List[str]:
        ...
