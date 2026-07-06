from typing import Protocol, runtime_checkable
from pydantic import BaseModel

class ProjectedView(BaseModel):
    content: str
    content_type: str

@runtime_checkable
class ProjectionEngine(Protocol):
    async def project(self, artifact_uri: str) -> ProjectedView:
        ...

class MarkdownProjection(ProjectionEngine):
    async def project(self, artifact_uri: str) -> ProjectedView:
        return ProjectedView(content="# Markdown Content", content_type="text/markdown")

class JSONProjection(ProjectionEngine):
    async def project(self, artifact_uri: str) -> ProjectedView:
        return ProjectedView(content="{}", content_type="application/json")
        
class EmbeddingProjection(ProjectionEngine):
    async def project(self, artifact_uri: str) -> ProjectedView:
        return ProjectedView(content="[0.1, 0.2, 0.3]", content_type="application/x-embedding")
