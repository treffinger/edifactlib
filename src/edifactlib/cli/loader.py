from pathlib import Path

from typer import Exit, echo

from ..core import Parser
from ..core.exceptions import EdifactError
from ..core.models.interchange import Interchange
from ..core.resolver import InterchangeResolver


def load_interchange_from_disk(path: Path) -> str:
    try:
        with path.open() as f:
            return f.read()
    except FileNotFoundError:
        echo(f'The file "{path}" could not be found.', err=True)
        raise Exit(1)


def parse_interchange(content: str) -> Interchange:
    parser = Parser()
    try:
        interchange = parser.parse(content)
    except EdifactError as e:
        echo(f"Failed to load the interchange. Error: {e}", err=True)
        raise Exit(1)

    resolver = InterchangeResolver()
    resolver.resolve(interchange)
    return interchange
