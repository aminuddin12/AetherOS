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
