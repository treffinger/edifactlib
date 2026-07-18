from typer import Typer

from .cli import run

app = Typer()
app.command()(run)

if __name__ == "__main__":
    app()
