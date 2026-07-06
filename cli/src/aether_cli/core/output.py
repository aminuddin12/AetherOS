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
