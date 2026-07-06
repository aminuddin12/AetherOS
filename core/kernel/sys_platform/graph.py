from typing import Dict, Set, List

class RuntimeDependencyError(Exception):
    pass

class RuntimeGraph:
    def __init__(self) -> None:
        self._nodes: Set[str] = set()
        self._adj: Dict[str, Set[str]] = {}

    def add_node(self, node: str) -> None:
        self._nodes.add(node)
        if node not in self._adj:
            self._adj[node] = set()

    def add_dependency(self, dependent: str, dependency: str) -> None:
        self.add_node(dependent)
        self.add_node(dependency)
        self._adj[dependent].add(dependency)

    def validate_and_sort(self) -> List[str]:
        in_degree: Dict[str, int] = {node: 0 for node in self._nodes}
        
        for u in self._nodes:
            for v in self._adj.get(u, set()):
                in_degree[v] = in_degree.get(v, 0) + 1
                
        queue: List[str] = [node for node, deg in in_degree.items() if deg == 0]
        order: List[str] = []
        
        while queue:
            u = queue.pop(0)
            order.append(u)
            
            for v in self._adj.get(u, set()):
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.append(v)
                    
        if len(order) != len(self._nodes):
            raise RuntimeDependencyError("Circular dependency detected in runtime graph")
            
        order.reverse()
        return order
