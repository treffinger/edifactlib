from __future__ import annotations

from pydantic import BaseModel

from .segment import Segment
from .service_characters import ServiceCharacters


class Message(BaseModel):
    header: Segment
    trailer: Segment
    segments: list[Segment]

    def dump_raw(self, service_chars: ServiceCharacters) -> str:
        raw = f"{self.header.dump_raw(service_chars)}{service_chars.segment_terminator}\n"
        raw += f"{service_chars.segment_terminator}\n".join(
            [segment.dump_raw(service_chars) for segment in self.segments]
        )
        raw += f"{service_chars.segment_terminator}\n{self.trailer.dump_raw(service_chars)}{service_chars.segment_terminator}"
        return raw
