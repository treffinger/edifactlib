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
        self,
        service_chars: ServiceCharacters | None = None,
        target: InterchangeBaseModel | None = None,
        style: Callable | None = None,
    ) -> str:
        """Serialize the interchange back into raw EDIFACT text.

        Args:
            service_chars: The service characters to use. If None, they are
                derived from the interchange's own UNA segment, or the
                defaults are used if there is none.
            target: A part of this model whose raw text should be passed
                to ``style``.
            style: A function that receives the raw text of ``target`` and
                returns a styled version of it, e.g. wrapped in ANSI color
                codes. If None, no styling is applied.

        Returns:
            The raw EDIFACT text of the interchange, one segment per line.
        """
        service_chars = service_chars or (ServiceCharacters.from_una(self.una) if self.una else ServiceCharacters())
        raw = f"{self.una.dump_raw(service_chars, target, style)}\n" if self.una else ""
        raw += f"{self.header.dump_raw(service_chars, target, style)}{service_chars.segment_terminator}\n"
        raw += "\n".join([fg.dump_raw(service_chars, target, style) for fg in self.functional_groups])
        raw += "\n".join([message.dump_raw(service_chars, target, style) for message in self.messages])
        raw += f"\n{self.trailer.dump_raw(service_chars, target, style)}{service_chars.segment_terminator}"
        return self._apply_style(raw, target, style)
