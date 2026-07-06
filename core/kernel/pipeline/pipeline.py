from typing import List, Any
from .middleware import PipelineMiddleware
from .hooks import PipelineHook
from core.kernel.context import KernelExecutionContext


class KernelExecutionPipeline:
    """
    Orkestrator eksekusi.
    Validation ➔ AuthZ ➔ Scheduling ➔ Dispatch ➔ Execution ➔ Metrics ➔ Completion.
    """

    def __init__(self):
        self._middlewares: List[PipelineMiddleware] = []
        self._hooks: List[PipelineHook] = []

    def use(self, middleware: PipelineMiddleware) -> None:
        self._middlewares.append(middleware)

    def add_hook(self, hook: PipelineHook) -> None:
        self._hooks.append(hook)

    async def execute(self, context: KernelExecutionContext, payload: Any) -> Any:
        # Dummy executor flow. Real implementation involves chaining middlewares.
        for hook in self._hooks:
            hook.on_before(context)

        result = None
        try:
            # invoke middlewares...
            result = "Success"
            for hook in self._hooks:
                hook.on_after(context, result)
            return result
        except Exception as e:
            for hook in self._hooks:
                hook.on_error(context, e)
            raise e
