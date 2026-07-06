import typer

app = typer.Typer(help="Scaffold new components.")

@app.command("workspace")
def new_workspace(name: str):
    print(f"Creating new workspace: {name}")

@app.command("plugin")
def new_plugin(name: str):
    print(f"Creating new plugin: {name}")
