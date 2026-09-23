from typing import Callable, override

from .interchange_base_model import InterchangeBaseModel
from .segment import Segment
from .service_characters import ServiceCharacters


class Message(InterchangeBaseModel):
    header: Segment
    trailer: Segment
    segments: list[Segment]

    @override
    def dump_raw(
        self,
        service_chars: ServiceCharacters | None = None,
        target: InterchangeBaseModel | None = None,
        style: Callable | None = None,
    ) -> str:
        service_chars = service_chars or ServiceCharacters()
        raw = f"{self.header.dump_raw(service_chars, target, style)}{service_chars.segment_terminator}\n"
        raw += f"{service_chars.segment_terminator}\n".join(
            [segment.dump_raw(service_chars, target, style) for segment in self.segments]
        )
        raw += f"{service_chars.segment_terminator}\n{self.trailer.dump_raw(service_chars, target, style)}{service_chars.segment_terminator}"
        return self._apply_style(raw, target, style)
