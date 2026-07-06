import os

files = {
    "cli/src/aether_cli/__init__.py": "",
    "cli/src/aether_cli/core/__init__.py": "",
    "cli/src/aether_cli/core/context.py": """
from dataclasses import dataclass
from typing import Any, Dict, Optional

@dataclass
class CommandContext:
    workspace_path: str
    user: str
    environment: str
    config: Dict[str, Any]
    output_format: str
    verbose: bool
""",
    "cli/src/aether_cli/core/output.py": """
import json
import yaml
from rich.console import Console
from rich.table import Table

console = Console()

class OutputFormatter:
    @staticmethod
    def format_output(data: dict, fmt: str = "text"):
        if fmt == "json":
            console.print(json.dumps(data, indent=2))
        elif fmt == "yaml":
            console.print(yaml.dump(data, default_flow_style=False))
        elif fmt == "table":
            table = Table()
            if not data:
                return
            keys = list(data.keys())
            for key in keys:
                table.add_column(key)
            table.add_row(*[str(data[k]) for k in keys])
            console.print(table)
        else:
            console.print(data)
""",
    "cli/src/aether_cli/core/metadata.py": """
from pydantic import BaseModel
from typing import List, Optional

class CommandMetadata(BaseModel):
    name: str
    description: str
    version: str = "1.0.0"
    experimental: bool = False
    deprecated: bool = False
    permissions: List[str] = []
""",
    "cli/src/aether_cli/core/events.py": """
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
""",
    "cli/src/aether_cli/core/registry.py": """
from typing import Callable, Dict

class CommandRegistry:
    def __init__(self):
        self.commands: Dict[str, Callable] = {}

    def register(self, name: str, func: Callable):
        self.commands[name] = func

    def get_all(self):
        return self.commands

registry = CommandRegistry()
""",
    "cli/src/aether_cli/core/pipeline.py": """
from typing import Callable
from .context import CommandContext
from .events import event_manager

class CommandPipeline:
    @staticmethod
    def execute(command: Callable, ctx: CommandContext, **kwargs):
        # 1. Validate
        
        # 2. Load Config (assume attached to ctx)
        
        # 3. Permission Check
        
        # 4. Trigger Before Event
        event_manager.dispatch("BeforeCommand", command=command.__name__, ctx=ctx)
        
        # 5. Execute
        result = command(ctx, **kwargs)
        
        # 6. Trigger After Event
        event_manager.dispatch("AfterCommand", command=command.__name__, result=result)
        
        # 7. Output Handling is usually done within command via Formatter
        return result
"""
}

for path, content in files.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content.strip() + "\n")
print("✅ Core files scaffolded.")
