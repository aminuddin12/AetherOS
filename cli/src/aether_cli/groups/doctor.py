import typer
import asyncio
from ..core.output import OutputFormatter
from aether_runtime.sdk import RuntimeBuilder

app = typer.Typer(help="Check AetherOS environment health.")
runtime = RuntimeBuilder().build()

@app.command("run")
def doctor_run(format: str = typer.Option("table", "--format", "-f", help="Output format")):
    async def _run():
        await runtime.start()
        diag = await runtime.diagnostics.environment()
        data = [item.model_dump() for item in diag.results]
        
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
        
        await runtime.stop()
    
    asyncio.run(_run())
