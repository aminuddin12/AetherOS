import typer
import asyncio
from ..core.output import OutputFormatter
from aether_runtime.sdk import RuntimeBuilder

app = typer.Typer(help="Inspect AetherOS internals.")
runtime = RuntimeBuilder().build()

@app.command("kernel")
def inspect_kernel(format: str = typer.Option("table", "--format", "-f", help="Output format (table, json, yaml)")):
    async def _run():
        await runtime.start()
        status = await runtime.kernel.status()
        OutputFormatter.format_output(status.model_dump(), fmt=format)
        await runtime.stop()
    asyncio.run(_run())

@app.command("execution")
def inspect_execution(format: str = typer.Option("table", "--format", "-f", help="Output format (table, json, yaml)")):
    async def _run():
        await runtime.start()
        status = await runtime.execution.status()
        OutputFormatter.format_output(status.model_dump(), fmt=format)
        await runtime.stop()
    asyncio.run(_run())

@app.command("graph")
def inspect_graph(format: str = typer.Option("mermaid", "--format", "-f", help="Output format (mermaid, dot, json)")):
    if format == "json":
        data = {"kernel": {}, "execution": {}, "workspace": {}}
        OutputFormatter.format_output(data, fmt="json")
    elif format == "mermaid":
        print("graph TD\nContracts --> Kernel\nKernel --> Execution\nExecution --> Workspace")
    else:
        print("Graph representation.")
