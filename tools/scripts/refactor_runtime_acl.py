import os

files = {
    "runtime/src/aether_runtime/adapters/__init__.py": "",
    "runtime/src/aether_runtime/adapters/kernel.py": """
from ..models.responses.kernel import KernelStatus, KernelServices

class KernelAdapter:
    @staticmethod
    def to_status_dto(raw_kernel_obj) -> KernelStatus:
        # Translates internal core.kernel objects to DTO
        return KernelStatus(
            version=raw_kernel_obj.get("version", "1.0.0"),
            status=raw_kernel_obj.get("status", "running"),
            uptime=raw_kernel_obj.get("uptime", 3600.0)
        )

    @staticmethod
    def to_services_dto(raw_services_list) -> KernelServices:
        return KernelServices(services=raw_services_list)
""",
    "runtime/src/aether_runtime/adapters/execution.py": """
from ..models.responses.execution import ExecutionStatus

class ExecutionAdapter:
    @staticmethod
    def to_status_dto(raw_engine_obj) -> ExecutionStatus:
        return ExecutionStatus(
            engine="Execution Engine",
            threads=raw_engine_obj.get("threads", 8),
            queues=raw_engine_obj.get("queues", 2),
            status=raw_engine_obj.get("status", "idle")
        )
""",
    "runtime/src/aether_runtime/services/__init__.py": "",
    "runtime/src/aether_runtime/services/kernel.py": """
from ..adapters.kernel import KernelAdapter

class KernelService:
    @staticmethod
    async def get_status():
        # Mock calling internal kernel
        raw_kernel = {"version": "1.0.0", "status": "running", "uptime": 3600.0}
        return KernelAdapter.to_status_dto(raw_kernel)

    @staticmethod
    async def get_services():
        raw_services = ["EventBus", "Scheduler", "StateManager"]
        return KernelAdapter.to_services_dto(raw_services)
""",
    "runtime/src/aether_runtime/services/execution.py": """
from ..adapters.execution import ExecutionAdapter

class ExecutionService:
    @staticmethod
    async def get_status():
        raw_engine = {"threads": 8, "queues": 2, "status": "idle"}
        return ExecutionAdapter.to_status_dto(raw_engine)
""",
    "runtime/src/aether_runtime/facade/kernel.py": """
from ..session.session import RuntimeSession
from ..middleware.pipeline import MiddlewarePipeline
from ..services.kernel import KernelService
from ..models.responses.kernel import KernelStatus, KernelServices

class KernelFacade:
    def __init__(self, session: RuntimeSession, pipeline: MiddlewarePipeline):
        self.session = session
        self.pipeline = pipeline

    async def status(self) -> KernelStatus:
        return await self.pipeline.execute(self.session, "kernel.status", KernelService.get_status)

    async def services(self) -> KernelServices:
        return await self.pipeline.execute(self.session, "kernel.services", KernelService.get_services)
""",
    "runtime/src/aether_runtime/facade/execution.py": """
from ..session.session import RuntimeSession
from ..middleware.pipeline import MiddlewarePipeline
from ..services.execution import ExecutionService
from ..models.responses.execution import ExecutionStatus

class ExecutionFacade:
    def __init__(self, session: RuntimeSession, pipeline: MiddlewarePipeline):
        self.session = session
        self.pipeline = pipeline

    async def status(self) -> ExecutionStatus:
        return await self.pipeline.execute(self.session, "execution.status", ExecutionService.get_status)
""",
    "runtime/src/aether_runtime/facade/diagnostics.py": """
from ..session.session import RuntimeSession
from ..middleware.pipeline import MiddlewarePipeline
from ..models.health.diagnostics import EnvironmentDiagnostics, DiagnosticItem

class DiagnosticsFacade:
    def __init__(self, session: RuntimeSession, pipeline: MiddlewarePipeline):
        self.session = session
        self.pipeline = pipeline

    async def environment(self) -> EnvironmentDiagnostics:
        async def _execute():
            items = [
                DiagnosticItem(check="Python Version", status="OK"),
                DiagnosticItem(check="uv installed", status="OK"),
                DiagnosticItem(check="Git", status="OK"),
                DiagnosticItem(check="Kernel Connection", status="OK")
            ]
            return EnvironmentDiagnostics(results=items)
        return await self.pipeline.execute(self.session, "diagnostics.environment", _execute)
""",
    "runtime/src/aether_runtime/sdk.py": """
from .context.context import RuntimeContext
from .session.session import RuntimeSession
from .middleware.pipeline import MiddlewarePipeline
from .facade.kernel import KernelFacade
from .facade.execution import ExecutionFacade
from .facade.diagnostics import DiagnosticsFacade
from .events.dispatcher import event_dispatcher
from .models.metadata.manifest import RuntimeManifest

class AetherRuntime:
    def __init__(self, context: RuntimeContext, session: RuntimeSession, pipeline: MiddlewarePipeline):
        self.context = context
        self.session = session
        self.pipeline = pipeline
        
        self.kernel = KernelFacade(self.session, self.pipeline)
        self.execution = ExecutionFacade(self.session, self.pipeline)
        self.diagnostics = DiagnosticsFacade(self.session, self.pipeline)

    async def capabilities(self) -> dict:
        return {
            "kernel": True,
            "execution": True,
            "workspace": False,
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
"""
}

for path, content in files.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content.strip() + "\n")

# Cleanup old client.py
if os.path.exists("runtime/src/aether_runtime/client.py"):
    os.remove("runtime/src/aether_runtime/client.py")

print("✅ Phase 3 & 4 ACL completed.")
