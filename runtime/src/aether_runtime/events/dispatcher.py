from typing import Callable, Dict, List

class RuntimeEventDispatcher:
    def __init__(self):
        self.listeners: Dict[str, List[Callable]] = {}

    def subscribe(self, event_name: str, callback: Callable):
        if event_name not in self.listeners:
            self.listeners[event_name] = []
        self.listeners[event_name].append(callback)

    async def dispatch(self, event_name: str, **kwargs):
        for callback in self.listeners.get(event_name, []):
            await callback(**kwargs)

    async def translate_and_dispatch(self, kernel_event: str, **kwargs):
        # Translate Kernel event to Runtime event
        event_map = {
            "KernelWorkerStarted": "RuntimeExecutionStarted",
            "KernelReady": "RuntimeReady"
        }
        runtime_event = event_map.get(kernel_event, kernel_event)
        await self.dispatch(runtime_event, **kwargs)

event_dispatcher = RuntimeEventDispatcher()
