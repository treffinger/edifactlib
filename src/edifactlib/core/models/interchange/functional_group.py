from pydantic import BaseModel

from .message import Message
from .segment import Segment


class FunctionalGroup(BaseModel):
    header: Segment
    trailer: Segment
    messages: list[Message]
