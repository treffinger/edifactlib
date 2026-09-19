from pydantic import BaseModel

from .message import Message
from .segment import Segment
from .service_characters import ServiceCharacters


class FunctionalGroup(BaseModel):
    header: Segment
    trailer: Segment
    messages: list[Message]

    def dump_raw(self, service_chars: ServiceCharacters) -> str:
        raw = f"{self.header.dump_raw(service_chars)}{service_chars.segment_terminator}\n"
        raw += "".join([message.dump_raw(service_chars) for message in self.messages])
        raw += f"\n{self.trailer.dump_raw(service_chars)}{service_chars.segment_terminator}"
        return raw
