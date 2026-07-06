from typing import Dict, List, Optional
from ..core.resources import WorkspaceNode, NodeType

class MemoryResourceProvider:
    def __init__(self):
        self._storage: Dict[str, WorkspaceNode] = {}

    async def put(self, node: WorkspaceNode):
        self._storage[node.id] = node

    async def get(self, node_id: str) -> Optional[WorkspaceNode]:
        return self._storage.get(node_id)

    async def list(self, type_filter: Optional[NodeType] = None) -> List[WorkspaceNode]:
        if type_filter:
            return [node for node in self._storage.values() if node.type == type_filter]
        return list(self._storage.values())

    async def delete(self, node_id: str):
        if node_id in self._storage:
            del self._storage[node_id]
