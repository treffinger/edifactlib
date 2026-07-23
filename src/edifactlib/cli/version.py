from importlib.metadata import version

from typer import Exit, echo


def print_version(value: bool) -> None:
    if not value:
        return

    echo(f"Version: {version("edifactlib")}")
    raise Exit()
