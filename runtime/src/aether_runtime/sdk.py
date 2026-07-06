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
from .capabilities import RuntimeCapabilities
from .kernel_integration import KernelIntegration
from .facade.workspace_app import WorkspaceAppFacade
from .facade.organization import OrganizationFacade
from .facade.knowledge import KnowledgeFacade
from .facade.provider_router import ProviderRouterFacade
from .facade.workflow import WorkflowFacade
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
        self.workspace_app = WorkspaceAppFacade(engine=None)  # Wired later by Bootstrap
        self.organization = OrganizationFacade()
        self.knowledge = KnowledgeFacade(
            artifact=self.artifact,
            repository=self.repository,
            storage=self.storage,
            workspace=self.workspace,
            organization=self.organization,
            runtime=self,
        )
        self.provider_router = ProviderRouterFacade()
        self.workflow = WorkflowFacade()
        self._kernel_integration = None

    async def capabilities(self) -> dict:
        """
        Get the runtime capabilities that can be registered with the kernel.
        
        Returns:
            Dictionary of capability descriptors that can be used for kernel registration.
        """
        capabilities = {}
        for cap in RuntimeCapabilities.get_capability_descriptors():
            capabilities[cap.id] = {
                "name": cap.name,
                "version": cap.version,
                "provider": cap.provider,
                "contract": cap.contract,
                "optional": cap.optional,
                "critical": cap.critical,
                "description": cap.description
            }
        return capabilities

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
    
    def register_with_kernel(self) -> List[str]:
        """
        Register runtime capabilities with the kernel.
        
        Returns:
            List of successfully registered capability IDs.
        """
        if not self._kernel_integration:
            raise RuntimeError("Kernel integration not initialized.")
        return self._kernel_integration.register_capabilities()
    
    def get_kernel_integration(self) -> KernelIntegration:
        """
        Get the kernel integration object.
        
        Returns:
            The KernelIntegration object.
        """
        return self._kernel_integration
    
    def is_capability_registered(self, capability_id: str) -> bool:
        """
        Check if a capability is registered with the kernel.
        
        Args:
            capability_id: The ID of the capability to check.
            
        Returns:
            True if capability is registered, False otherwise.
        """
        if not self._kernel_integration:
            return False
        return self._kernel_integration.is_capability_registered(capability_id)


class RuntimeBuilder:
    def __init__(self):
        self._context = RuntimeContext()
        self._session = None
        self._pipeline = MiddlewarePipeline()
        self._kernel = None
        self._kernel_integration = KernelIntegration()

    def with_context(self, context: RuntimeContext):
        self._context = context
        return self

    def with_kernel(self, kernel):
        self._kernel = kernel
        self._kernel_integration.set_kernel_bridge(kernel)
        return self
    
    def with_kernel_integration(self, kernel_integration: KernelIntegration):
        self._kernel_integration = kernel_integration
        return self

    def add_middleware(self, middleware):
        self._pipeline.use(middleware)
        return self

    def build(self) -> AetherRuntime:
        session = self._session or RuntimeSession(self._context)
        runtime = AetherRuntime(self._context, session, self._pipeline)
        runtime._kernel_integration = self._kernel_integration
        return runtime
