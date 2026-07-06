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
