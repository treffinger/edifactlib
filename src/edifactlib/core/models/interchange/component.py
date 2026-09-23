from typing import Callable, override

from .interchange_base_model import InterchangeBaseModel
from .service_characters import ServiceCharacters


class Component(InterchangeBaseModel):
    content: str | None
    name: str | None = None

    @override
    def dump_raw(
        self,
        service_chars: ServiceCharacters | None = None,
        target: InterchangeBaseModel | None = None,
        style: Callable | None = None,
    ) -> str:
        if not self.content:
            return ""

        service_chars = service_chars or ServiceCharacters()
        reserved = {
            service_chars.component_sep,
            service_chars.data_element_sep,
            service_chars.segment_terminator,
            service_chars.release_indicator,
        }
        raw = "".join(f"{service_chars.release_indicator}{c}" if c in reserved else c for c in self.content)
        return self._apply_style(raw, target, style)
