from pathlib import Path
from typing import Annotated

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.tree import Tree
from typer import Argument, BadParameter, Context, Exit, Option, echo

from ..core import Parser
from ..core.exceptions import EdifactError
from ..core.models.interchange import Interchange, Message, Segment
from ..core.resolver import InterchangeResolver


def run(
    ctx: Context,
    path: Annotated[str | None, Argument(help="EDIFACT message file path")] = None,
    from_string: Annotated[str | None, Option(help="EDIFACT message as String")] = None,
    print_json: Annotated[bool, Option(help="Prints the interchange as JSON")] = False,
) -> None:
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


def print_interchange(interchange: Interchange) -> None:
    console = Console()
    console.print(Panel.fit("Interchange", style="bold blue"))
    header_table = create_interchange_header_table(interchange.header)
    console.print(header_table)

    if len(interchange.messages) > 0:
        tree = Tree("[green]Messages[/green]")
        for m in interchange.messages:
            tree.add(Panel.fit(create_message_tree_node(m)))
        console.print(tree)

    if len(interchange.functional_groups) > 0:
        tree = Tree("[green]Functional groups[/green]")
        for fg in interchange.functional_groups:
            node = Tree("[green]Group[/green]")
            tree.add(node)
            for m in fg.messages:
                node.add(Panel.fit(create_message_tree_node(m)))
        console.print(tree)


def create_interchange_header_table(header: Segment) -> Table:
    table = Table(title="Interchange information", box=box.ROUNDED)
    table.add_column("Attribute")
    table.add_column("Value", style="dim")

    # Syntax identifier
    table.add_row("Syntax identifier", header.data_elements[0].components[0].content)

    # Interchange sender
    value = f"[bold]Sender identification:[/bold] {header.data_elements[1].components[0].content}\n"
    if len(header.data_elements[1].components) > 1:
        value += f"[bold]Partner identification:[/bold] {header.data_elements[1].components[1].content or "-"}"
    if len(header.data_elements[1].components) > 2:
        value += f"[bold]Address for reverse routing:[/bold] {header.data_elements[1].components[2].content or "-"}"
    table.add_row("Interchange sender", value)

    # Interchange recipient
    value = f"[bold]Recipient Identification:[/bold] {header.data_elements[2].components[0].content}\n"
    if len(header.data_elements[2].components) > 1:
        value += f"[bold]Partner identification:[/bold] {header.data_elements[2].components[1].content or "-"}"
    if len(header.data_elements[2].components) > 2:
        value += f"[bold]Routing address:[/bold] {header.data_elements[2].components[2].content or "-"}"
    table.add_row("Interchange recipient", value)

    # Date / time of preparation
    date = header.data_elements[3].components[0].content
    time = header.data_elements[3].components[1].content
    if not date or not time:
        raise ValueError
    table.add_row(
        "Date/Time of preparation",
        f"[bold]Date (YY.MM.DD):[/bold] {date[0:2]}.{date[2:4]}.{date[4:6]}\n"
        f"[bold]Time:[/bold] {time[0:2]}:{time[2:4]}",
    )

    return table


def create_message_tree_node(message: Message) -> Tree:
    dir_name = f"{ message.header.data_elements[1].components[1].content}.{ message.header.data_elements[1].components[2].content}"
    table = Table(title="Message information", box=box.SIMPLE)
    table.add_column("Attribute")
    table.add_column("Value", style="dim")

    # Message reference number
    table.add_row("Message reference number", message.header.data_elements[0].components[0].content)

    # Message Identifier
    msg_identifier = message.header.data_elements[1]
    value = (
        f"[bold]Message type:[/bold] {msg_identifier.components[0].content}\n"
        f"[bold]Directory:[/bold] {dir_name}\n"
        f"[bold]Controlling agency:[/bold] {msg_identifier.components[3].content}"
    )
    if len(msg_identifier.components) == 5:
        value += f"[bold]Association assigned:[/bold] {msg_identifier.components[4].content}"
    table.add_row("Message identifier", value)

    tree = Tree(table)
    for segment in message.segments:
        tree.add(create_segment_tree_node(segment, dir_name))

    return tree


def create_segment_tree_node(segment: Segment, dir_name: str) -> Tree:
    tree = Tree(f"[bold cyan]{segment.tag}[/] ({segment.name})")

    for element in segment.data_elements:
        if not len(element.components):
            continue
        elif len(element.components) == 1:
            tree.add(f"{element.name}: [dim]{element.components[0].content}[/dim]")
        else:
            sub = tree.add(f"[cyan]{element.name}[/cyan]")
            for component in element.components:
                if component.content is not None:
                    sub.add(f"{component.name}: [dim]{component.content}[/dim]")
    return tree
