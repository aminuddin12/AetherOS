from .context import WorkspaceContext
from .environment import WorkspaceEnvironment
from .diagnostics import WorkspaceDiagnostics

class WorkspaceAggregateRoot:
    def __init__(self, context: WorkspaceContext, env: WorkspaceEnvironment):
        self.context = context
        self.environment = env
        self.diagnostics = WorkspaceDiagnostics()
