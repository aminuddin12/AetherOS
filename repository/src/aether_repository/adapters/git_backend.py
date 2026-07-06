from ..protocols.backend import RepositoryBackend
from ..core.domain import Commit, Diff, History
from ..references.models import RepositoryReference, RevisionReference
from typing import List

class GitRepositoryBackend:
    """Stub implementation of Git RepositoryBackend."""
    
    async def initialize(self, uri: str) -> RepositoryReference:
        raise NotImplementedError
    async def clone(self, source_uri: str, target_uri: str) -> RepositoryReference:
        raise NotImplementedError
    async def fetch(self, repo: RepositoryReference) -> None: pass
    async def push(self, repo: RepositoryReference) -> None: pass
    async def pull(self, repo: RepositoryReference) -> None: pass
    async def checkout(self, revision: RevisionReference) -> None: pass
    async def commit(self, repo: RepositoryReference, message: str, tree_uri: str) -> Commit:
        raise NotImplementedError
    async def merge(self, source: RevisionReference, target: RevisionReference) -> Commit:
        raise NotImplementedError
    async def diff(self, base: RevisionReference, target: RevisionReference) -> Diff:
        raise NotImplementedError
    async def history(self, revision: RevisionReference) -> History:
        raise NotImplementedError
    async def references(self, repo: RepositoryReference) -> List[str]:
        return []
