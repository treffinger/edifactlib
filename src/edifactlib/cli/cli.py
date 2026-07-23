from pathlib import Path
from typing import Annotated

from typer import Argument, BadParameter, Context, Exit, Option, echo

from ..core.models.interchange import Interchange
from .loader import load_interchange_from_disk, parse_interchange
from .renderer import print_interchange
from .version import print_version


def run(
    ctx: Context,
    path: Annotated[str | None, Argument(help="EDIFACT message file path")] = None,
    from_string: Annotated[str | None, Option(help="EDIFACT message as String")] = None,
    print_json: Annotated[bool, Option(help="Prints the interchange as JSON")] = False,
    version: Annotated[
        bool, Option(callback=print_version, is_eager=True, help="Displays the version of edifactlib")
    ] = False,
) -> None:
    """
    The edifact tool loads, validates, and displays UN/EDIFACT interchanges on the console.

    Provide the interchange either as a file by entering its path or inline via --from-string.
    """
    if not path and not from_string:
        echo(ctx.get_help())
        raise Exit()
    elif path is not None and from_string is not None:
        raise BadParameter('Use either "edifact /path/to/file.txt" or "edifact --from-string \'...\'".')

    interchange: Interchange | None = None

    if path is not None:
        interchange = parse_interchange(load_interchange_from_disk(Path(path)))
    elif from_string is not None:
        interchange = parse_interchange(from_string)

    if not interchange:
        return

    if print_json:
        echo(interchange.model_dump_json())
    else:
        print_interchange(interchange)
