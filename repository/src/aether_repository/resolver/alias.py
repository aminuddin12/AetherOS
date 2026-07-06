from ..references.models import RevisionReference
from typing import Protocol, runtime_checkable

@runtime_checkable
class AliasResolver(Protocol):
    """Protocol for resolving string aliases into concrete RevisionReferences."""
    async def resolve_alias(self, repository_uri: str, alias: str) -> RevisionReference:
        ...

class GenericResolver(AliasResolver):
    """Generic resolver capable of resolving HEAD, HEAD~N, branch names, tags, etc."""
    async def resolve_alias(self, repository_uri: str, alias: str) -> RevisionReference:
        # Stub implementation. Real implementation delegates to the underlying backend graph.
        return RevisionReference(repository_uri=repository_uri, revision_id=f"resolved_{alias}")
