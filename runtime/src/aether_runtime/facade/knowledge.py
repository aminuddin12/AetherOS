from typing import Any, Dict, List, Optional
from ..services.knowledge import KnowledgeService
from ..models.responses.knowledge import KnowledgeGraphSummary, KnowledgeQueryResult, KnowledgeResource


class KnowledgeFacade:
    """Public interface for Company Brain orchestration (Milestone 4)."""

    def __init__(
        self,
        artifact=None,
        repository=None,
        storage=None,
        workspace=None,
        organization=None,
        runtime=None,
    ) -> None:
        self.artifact = artifact
        self.repository = repository
        self.storage = storage
        self.workspace = workspace
        self.organization = organization
        self._runtime = runtime
        self._service = KnowledgeService(runtime=runtime)

    async def index(
        self,
        uri: str,
        title: str,
        summary: str,
        tags: List[str] | None = None,
        metadata: Dict[str, Any] | None = None,
    ) -> str:
        """Index a knowledge node referenced by a universal resource URI."""
        return await self._service.index(uri, title, summary, tags=tags, metadata=metadata)

    async def index_resource(
        self,
        uri: str,
        tags: List[str] | None = None,
        metadata: Dict[str, Any] | None = None,
    ) -> KnowledgeResource:
        """Resolve a runtime resource URI and ingest it into Company Brain using runtime services."""
        return await self._service.index_resource(uri, tags=tags, metadata=metadata)

    async def query(
        self,
        query_text: str,
        limit: int = 5,
        workspace_id: Optional[str] = None,
    ) -> KnowledgeQueryResult:
        """Query cached knowledge nodes using a lightweight semantic matcher."""
        return await self._service.query(query_text, limit=limit, workspace_id=workspace_id)

    async def summarize(self) -> KnowledgeGraphSummary:
        """Return summary metadata for the in-memory knowledge graph."""
        return await self._service.summarize_graph()

    async def infer_relationship(
        self,
        source_uri: str,
        predicate: str,
        target_uri: str,
    ) -> Dict[str, str]:
        """Create a semantic relationship between two knowledge nodes."""
        return await self._service.add_edge(source_uri, predicate, target_uri)

    async def describe(self, uri: str) -> Dict[str, Any]:
        """Describe the indexed node for a given resource URI."""
        return await self._service.describe(uri)
