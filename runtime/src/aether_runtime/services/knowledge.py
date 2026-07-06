from typing import Any, Dict, List, Optional
from ..models.responses.knowledge import KnowledgeDocument, KnowledgeQueryResult, KnowledgeGraphSummary, KnowledgeResource


class KnowledgeService:
    def __init__(self, runtime: Optional[Any] = None) -> None:
        self._documents: Dict[str, KnowledgeDocument] = {}
        self._edges: List[Dict[str, str]] = []
        self._runtime = runtime

    async def index(
        self,
        uri: str,
        title: str,
        summary: str,
        tags: List[str] | None = None,
        metadata: Dict[str, Any] | None = None,
    ) -> str:
        tags = tags or []
        metadata = metadata or {}

        document = KnowledgeDocument(
            uri=uri,
            title=title,
            summary=summary,
            tags=tags,
            metadata=metadata,
        )

        self._documents[uri] = document
        return uri

    async def query(
        self,
        query: str,
        limit: int = 5,
        workspace_id: str | None = None,
    ) -> KnowledgeQueryResult:
        lower_query = query.lower()
        scored_documents: List[tuple[float, KnowledgeDocument]] = []

        for document in self._documents.values():
            score = 0.0
            if lower_query in document.title.lower():
                score += 3.0
            if lower_query in document.summary.lower():
                score += 1.5
            for tag in document.tags:
                if lower_query in tag.lower():
                    score += 0.5

            if score > 0.0:
                scored_documents.append((score, document))

        scored_documents.sort(key=lambda item: item[0], reverse=True)
        results = [document for _, document in scored_documents[:limit]]
        scored = {document.uri: score for score, document in scored_documents[:limit]}

        return KnowledgeQueryResult(
            query=query,
            results=results,
            total=len(scored_documents),
            scored=scored,
        )

    async def summarize_graph(self) -> KnowledgeGraphSummary:
        known_domains = sorted(
            {
                uri.split("://")[0]
                if "://" in uri
                else "unknown"
                for uri in self._documents.keys()
            }
        )

        return KnowledgeGraphSummary(
            node_count=len(self._documents),
            edge_count=len(self._edges),
            known_domains=known_domains,
        )

    async def add_edge(self, source_uri: str, predicate: str, target_uri: str) -> Dict[str, str]:
        relationship = {
            "source": source_uri,
            "predicate": predicate,
            "target": target_uri,
        }
        self._edges.append(relationship)
        return relationship

    async def describe(self, uri: str) -> Dict[str, Any]:
        document = self._documents.get(uri)
        return document.model_dump() if document else {}

    async def index_resource(
        self,
        uri: str,
        tags: List[str] | None = None,
        metadata: Dict[str, Any] | None = None,
    ) -> KnowledgeResource:
        """Resolve a runtime resource URI and aggregate information from all runtime services."""
        tags = tags or []
        metadata = metadata or {}
        
        if not self._runtime:
            # Fallback to basic indexing if runtime not available
            return KnowledgeResource(
                uri=uri,
                identifier=uri,
                title=uri,
                summary="Resource resolved without runtime services",
                artifact_info={},
                repository_graph={},
                workspace_context={},
                storage_metadata={},
                organization_info={}
            )
        
        try:
            # Step 1: Resolve artifact URI to get identifier
            identifier = uri  # Default to URI if resolution fails
            artifact_info = {}
            
            if hasattr(self._runtime.artifact, 'resolve'):
                try:
                    artifact_result = await self._runtime.artifact.resolve(uri)
                    if isinstance(artifact_result, dict):
                        identifier = artifact_result.get("identifier", uri)
                        artifact_info = artifact_result
                    else:
                        # Handle case where resolve returns non-dict (e.g., string)
                        artifact_info = {"resolved": str(artifact_result)}
                except Exception as e:
                    print(f"Artifact resolution failed: {e}")
            
            # Step 2: Get repository graph
            repository_graph = {}
            if hasattr(self._runtime.repository, 'graph'):
                try:
                    repository_graph = await self._runtime.repository.graph(identifier)
                except Exception as e:
                    print(f"Repository graph failed: {e}")
            
            # Step 3: Get workspace context
            workspace_context = {}
            if hasattr(self._runtime.workspace, 'describe'):
                try:
                    workspace_context = await self._runtime.workspace.describe(identifier)
                except Exception as e:
                    print(f"Workspace context failed: {e}")
            
            # Step 4: Get storage metadata
            storage_metadata = {}
            if hasattr(self._runtime.storage, 'resolve'):
                try:
                    storage_result = await self._runtime.storage.resolve(identifier)
                    if isinstance(storage_result, dict):
                        storage_metadata = storage_result
                    else:
                        # Handle case where resolve returns a string (URI)
                        storage_metadata = {"uri": str(storage_result)}
                except Exception as e:
                    print(f"Storage resolution failed: {e}")
            
            # Step 5: Get organization info
            organization_info = {}
            if hasattr(self._runtime.organization, 'identity'):
                try:
                    organization_info = await self._runtime.organization.identity()
                except Exception as e:
                    print(f"Organization identity failed: {e}")
            
            # Generate title and summary from aggregated data
            title_parts = []
            summary_parts = []
            
            # Safely access dictionary values
            artifact_name = artifact_info.get("name") if isinstance(artifact_info, dict) else None
            if artifact_name:
                title_parts.append(artifact_name)
            
            repository_revisions = repository_graph.get("revisions") if isinstance(repository_graph, dict) else None
            if repository_revisions:
                summary_parts.append(f"Repository with {len(repository_revisions)} revisions")
            
            workspace_name = workspace_context.get("name") if isinstance(workspace_context, dict) else None
            workspace_owner = workspace_context.get("owner") if isinstance(workspace_context, dict) else None
            if workspace_name:
                title_parts.append(f"in {workspace_name}")
                summary_parts.append(f"Workspace: {workspace_owner or 'unknown'}")
            
            if storage_metadata:
                storage_uri = storage_metadata.get('uri', 'resolved') if isinstance(storage_metadata, dict) else 'resolved'
                summary_parts.append(f"Storage: {storage_uri}")
            
            org_status = organization_info.get("status") if isinstance(organization_info, dict) else None
            if org_status:
                summary_parts.append(f"Organization: {org_status}")
            
            title = " ".join(title_parts) if title_parts else uri
            summary = ", ".join(summary_parts) if summary_parts else "Runtime resource"
            
            # Create the aggregated resource
            resource = KnowledgeResource(
                uri=uri,
                identifier=identifier,
                artifact_info=artifact_info,
                repository_graph=repository_graph,
                workspace_context=workspace_context,
                storage_metadata=storage_metadata,
                organization_info=organization_info,
                title=title,
                summary=summary
            )
            
            # Also index it as a document for backward compatibility
            await self.index(
                uri=uri,
                title=title,
                summary=summary,
                tags=tags,
                metadata={
                    "resource": resource.model_dump(),
                    **metadata
                }
            )
            
            return resource
            
        except Exception as e:
            # Graceful degradation - return basic resource
            print(f"Runtime resource resolution failed: {e}")
            return KnowledgeResource(
                uri=uri,
                identifier=uri,
                title=uri,
                summary=f"Resource resolution failed: {str(e)}",
                artifact_info={},
                repository_graph={},
                workspace_context={},
                storage_metadata={},
                organization_info={}
            )
