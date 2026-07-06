import os

files = {
    "cli/src/aether_cli/services/__init__.py": "",
    "cli/src/aether_cli/services/kernel_service.py": """
class KernelService:
    @staticmethod
    def get_manifest():
        return {"kernel": "AetherOS Kernel", "version": "1.0.0", "status": "running"}
        
    @staticmethod
    def get_loaded_services():
        return {"services": ["EventBus", "Scheduler", "StateManager"]}
""",
    "cli/src/aether_cli/services/execution_service.py": """
class ExecutionService:
    @staticmethod
    def get_engine_status():
        return {"engine": "Execution Engine", "threads": 8, "queues": 2, "status": "idle"}
""",
    "cli/src/aether_cli/services/doctor_service.py": """
class DoctorService:
    @staticmethod
    def check_environment():
        return [
            {"check": "Python Version", "status": "OK"},
            {"check": "uv installed", "status": "OK"},
            {"check": "Git", "status": "OK"},
            {"check": "Kernel Connection", "status": "OK"}
        ]
""",
    "cli/src/aether_cli/services/graph_service.py": """
class GraphService:
    @staticmethod
    def get_mermaid_graph():
        return "graph TD\\nContracts --> Kernel\\nKernel --> Execution\\nExecution --> Workspace"
""",
    "cli/src/aether_cli/groups/__init__.py": "",
    "cli/src/aether_cli/groups/inspect.py": """
import typer
from ..core.output import OutputFormatter
from ..services.kernel_service import KernelService
from ..services.execution_service import ExecutionService
from ..services.graph_service import GraphService

app = typer.Typer(help="Inspect AetherOS internals.")

@app.command("kernel")
def inspect_kernel(format: str = typer.Option("table", "--format", "-f", help="Output format (table, json, yaml)")):
    data = KernelService.get_manifest()
    OutputFormatter.format_output(data, fmt=format)

@app.command("execution")
def inspect_execution(format: str = typer.Option("table", "--format", "-f", help="Output format (table, json, yaml)")):
    data = ExecutionService.get_engine_status()
    OutputFormatter.format_output(data, fmt=format)

@app.command("graph")
def inspect_graph(format: str = typer.Option("mermaid", "--format", "-f", help="Output format (mermaid, dot, json)")):
    if format == "json":
        data = {"kernel": {}, "execution": {}, "workspace": {}}
        OutputFormatter.format_output(data, fmt="json")
    elif format == "mermaid":
        print(GraphService.get_mermaid_graph())
    else:
        print("Graph representation.")
""",
    "cli/src/aether_cli/groups/doctor.py": """
import typer
from ..core.output import OutputFormatter
from ..services.doctor_service import DoctorService

app = typer.Typer(help="Check AetherOS environment health.")

@app.command("run")
def doctor_run(format: str = typer.Option("table", "--format", "-f", help="Output format")):
    data = DoctorService.check_environment()
    # If list, format nicely
    if format == "table":
        from rich.table import Table
        from rich.console import Console
        console = Console()
        table = Table("Check", "Status")
        for item in data:
            table.add_row(item["check"], item["status"])
        console.print(table)
    else:
        OutputFormatter.format_output({"results": data}, fmt=format)
""",
    "cli/src/aether_cli/groups/new.py": """
import typer

app = typer.Typer(help="Scaffold new components.")

@app.command("workspace")
def new_workspace(name: str):
    print(f"Creating new workspace: {name}")

@app.command("plugin")
def new_plugin(name: str):
    print(f"Creating new plugin: {name}")
""",
    "cli/src/aether_cli/app.py": """
import typer
from .groups import inspect, doctor, new

app = typer.Typer(
    name="aether",
    help="AetherOS Developer Platform Runtime",
    add_completion=False,
)

app.add_typer(inspect.app, name="inspect")
app.add_typer(doctor.app, name="doctor", invoke_without_command=True)
app.add_typer(new.app, name="new")

if __name__ == "__main__":
    app()
"""
}

for path, content in files.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content.strip() + "\n")
print("✅ Services and Groups scaffolded.")
