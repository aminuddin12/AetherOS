from typing import Callable, Dict, List, Any
import asyncio

class WorkspaceBus:
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}

    def subscribe(self, topic: str, handler: Callable):
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(handler)

    async def publish(self, topic: str, payload: Any):
        if topic in self.subscribers:
            # Broadcast asynchronously
            tasks = [handler(payload) for handler in self.subscribers[topic]]
            await asyncio.gather(*tasks)

# Default bus instance
workspace_bus = WorkspaceBus()
