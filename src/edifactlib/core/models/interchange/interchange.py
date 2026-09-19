from pydantic import BaseModel

from .functional_group import FunctionalGroup
from .message import Message
from .segment import Segment
from .service_characters import ServiceCharacters


class Interchange(BaseModel):
    una: Segment | None = None
    header: Segment
    trailer: Segment
    functional_groups: list[FunctionalGroup] = []
    messages: list[Message] = []

    def dump_raw(self) -> str:
        service_chars = ServiceCharacters.from_una(self.una) if self.una else ServiceCharacters()
        raw = f"{self.una.dump_raw(service_chars)}\n" if self.una else ""
        raw += f"{self.header.dump_raw(service_chars)}{service_chars.segment_terminator}\n"
        raw += "".join([fg.dump_raw(service_chars) for fg in self.functional_groups])
        raw += "".join([message.dump_raw(service_chars) for message in self.messages])
        raw += f"\n{self.trailer.dump_raw(service_chars)}{service_chars.segment_terminator}"
        return raw
