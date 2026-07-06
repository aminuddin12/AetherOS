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
