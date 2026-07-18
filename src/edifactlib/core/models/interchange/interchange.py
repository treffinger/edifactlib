from pydantic import BaseModel

from .functional_group import FunctionalGroup
from .message import Message
from .segment import Segment


class Interchange(BaseModel):
    una: Segment | None = None
    header: Segment
    trailer: Segment
    functional_groups: list[FunctionalGroup] = []
    messages: list[Message] = []
