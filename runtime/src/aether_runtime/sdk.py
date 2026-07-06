from .context.context import RuntimeContext
from .session.session import RuntimeSession
from .middleware.pipeline import MiddlewarePipeline
from .facade.kernel import KernelFacade
from .facade.execution import ExecutionFacade
from .facade.diagnostics import DiagnosticsFacade
from .facade.workspace import WorkspaceFacade
from .facade.storage import StorageFacade
from .facade.repository import RepositoryFacade
from .facade.artifact import ArtifactFacade
from .facade.workspace_app import WorkspaceAppFacade
from .facade.organization import OrganizationFacade
from .events.dispatcher import event_dispatcher
from .models.metadata.manifest import RuntimeManifest

class AetherRuntime:
    """
    The main entry point for interacting with AetherOS (Milestone 2.7+).
    This acts as a high-level SDK providing access to isolated Domain Facades.
    """
    def __init__(self, context: RuntimeContext, session: RuntimeSession, pipeline: MiddlewarePipeline):
        self.context = context
        self.session = session
        self.pipeline = pipeline
        
        self.kernel = KernelFacade(self.session, self.pipeline)
        self.execution = ExecutionFacade(self.session, self.pipeline)
        self.diagnostics = DiagnosticsFacade(self.session, self.pipeline)
        self.workspace = WorkspaceFacade(self.session, self.pipeline)
        self.storage = StorageFacade()
        self.repository = RepositoryFacade()
        self.artifact = ArtifactFacade()
        self.workspace_app = WorkspaceAppFacade(engine=None) # Wired later by Bootstrap
        self.organization = OrganizationFacade()

    async def capabilities(self) -> dict:
        return {
            "kernel": True,
            "execution": True,
            "workspace": True,
            "knowledge": False
        }

    async def manifest(self) -> RuntimeManifest:
        return RuntimeManifest(
            runtime_version="1.0.0",
            kernel_version="1.0.0",
            contracts_version="1.0.0",
            execution_version="1.0.0",
            workspace_version="not-installed",
            compatibility="stable"
        )

    async def start(self):
        await self.session.start()
        await event_dispatcher.dispatch("RuntimeStarted", session_id=self.context.correlation_id)

    async def stop(self):
        await self.session.stop()
        await event_dispatcher.dispatch("RuntimeShutdown", session_id=self.context.correlation_id)


class RuntimeBuilder:
    def __init__(self):
        self._context = RuntimeContext()
        self._session = None
        self._pipeline = MiddlewarePipeline()
        self._kernel = None

    def with_context(self, context: RuntimeContext):
        self._context = context
        return self

    def with_kernel(self, kernel):
        self._kernel = kernel
        return self

    def add_middleware(self, middleware):
        self._pipeline.use(middleware)
        return self

    def build(self) -> AetherRuntime:
        session = self._session or RuntimeSession(self._context)
        return AetherRuntime(self._context, session, self._pipeline)
