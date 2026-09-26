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
        lines = [self.header, *self.segments, self.trailer]
        raw = "\n".join(
            [f"{segment.dump_raw(service_chars, target, style)}{service_chars.segment_terminator}" for segment in lines]
        )

        return self._apply_style(raw, target, style)
