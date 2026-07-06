from pydantic import BaseModel
from typing import List, Dict
from ..core.domain import Commit, Branch

class RevisionNode(BaseModel):
    commit_id: str
    parents: List[str]
    children: List[str]

class RevisionGraph(BaseModel):
    """Directed Acyclic Graph of all revisions."""
    nodes: Dict[str, RevisionNode]

class BranchGraph(BaseModel):
    """Topological representation of branches and their divergence points."""
    divergence_points: Dict[str, str] # branch_name -> commit_id
    hierarchy: Dict[str, List[str]]   # parent_branch -> list of child_branches

class MergeGraph(BaseModel):
    """Tracks merge points to resolve dependency flows between branches."""
    merges: List[Dict[str, str]] # [{'source': 'A', 'target': 'B', 'merge_commit': 'C'}]

class DependencyGraph(BaseModel):
    """Tracks how specific changes or files affect other parts of the repository."""
    dependencies: Dict[str, List[str]] # resource_uri -> list of dependent resource_uris

class RepositoryGraph(BaseModel):
    """Master aggregate graph containing all sub-graphs for Company Brain analysis."""
    revisions: RevisionGraph
    branches: BranchGraph
    merges: MergeGraph
    dependencies: DependencyGraph
