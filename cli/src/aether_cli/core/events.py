class CLIEventManager:
    def __init__(self):
        self.listeners = {}

    def subscribe(self, event_name: str, callback):
        if event_name not in self.listeners:
            self.listeners[event_name] = []
        self.listeners[event_name].append(callback)

    def dispatch(self, event_name: str, **kwargs):
        for callback in self.listeners.get(event_name, []):
            callback(**kwargs)

event_manager = CLIEventManager()
