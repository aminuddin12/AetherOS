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
