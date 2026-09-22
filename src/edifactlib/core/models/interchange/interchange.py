from typing import Callable, override

from .functional_group import FunctionalGroup
from .interchange_base_model import InterchangeBaseModel
from .message import Message
from .segment import Segment
from .service_characters import ServiceCharacters


class Interchange(InterchangeBaseModel):
    una: Segment | None = None
    header: Segment
    trailer: Segment
    functional_groups: list[FunctionalGroup] = []
    messages: list[Message] = []

    @override
    def dump_raw(
        self, service_chars: ServiceCharacters | None, target: InterchangeBaseModel | None, style: Callable | None
    ) -> str:
        service_chars = ServiceCharacters.from_una(self.una) if self.una else ServiceCharacters()
        raw = f"{self.una.dump_raw(service_chars, target, style)}\n" if self.una else ""
        raw += f"{self.header.dump_raw(service_chars, target, style)}{service_chars.segment_terminator}\n"
        raw += "".join([fg.dump_raw(service_chars, target, style) for fg in self.functional_groups])
        raw += "".join([message.dump_raw(service_chars, target, style) for message in self.messages])
        raw += f"\n{self.trailer.dump_raw(service_chars, target, style)}{service_chars.segment_terminator}"
        return self._apply_style(raw, target, style)
