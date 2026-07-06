from ..core.aggregate import WorkspaceAggregateRoot
from ..core.context import WorkspaceContext
from ..core.environment import WorkspaceEnvironment

class WorkspaceBuilder:
    def build(self, context: WorkspaceContext) -> WorkspaceAggregateRoot:
        env = WorkspaceEnvironment()
        return WorkspaceAggregateRoot(context, env)
