from typing import Callable, Dict

class CommandRegistry:
    def __init__(self):
        self.commands: Dict[str, Callable] = {}

    def register(self, name: str, func: Callable):
        self.commands[name] = func

    def get_all(self):
        return self.commands

registry = CommandRegistry()
