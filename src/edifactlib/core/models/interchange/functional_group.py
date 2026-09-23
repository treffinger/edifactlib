from typing import Callable, override

from .interchange_base_model import InterchangeBaseModel
from .message import Message
from .segment import Segment
from .service_characters import ServiceCharacters


class FunctionalGroup(InterchangeBaseModel):
    header: Segment
    trailer: Segment
    messages: list[Message]

    @override
    def dump_raw(
        self,
        service_chars: ServiceCharacters | None = None,
        target: InterchangeBaseModel | None = None,
        style: Callable | None = None,
    ) -> str:
        service_chars = service_chars or ServiceCharacters()
        raw = f"{self.header.dump_raw(service_chars, target, style)}{service_chars.segment_terminator}\n"
        raw += "".join([message.dump_raw(service_chars, target, style) for message in self.messages])
        raw += f"\n{self.trailer.dump_raw(service_chars, target, style)}{service_chars.segment_terminator}"
        return self._apply_style(raw, target, style)
