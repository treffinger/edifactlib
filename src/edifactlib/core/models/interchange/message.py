from pydantic import BaseModel

from .segment import Segment


class Message(BaseModel):
    header: Segment
    trailer: Segment
    segments: list[Segment]
