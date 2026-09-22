from __future__ import annotations

from typing import TYPE_CHECKING, Callable, override

from .interchange_base_model import InterchangeBaseModel

if TYPE_CHECKING:
    from .service_characters import ServiceCharacters


class Component(InterchangeBaseModel):
    content: str | None
    name: str | None = None

    @override
    def dump_raw(
        self, service_chars: ServiceCharacters, target: InterchangeBaseModel | None, style: Callable | None
    ) -> str:
        if not self.content:
            return ""

        reserved = {
            service_chars.component_sep,
            service_chars.data_element_sep,
            service_chars.segment_terminator,
            service_chars.release_indicator,
        }
        raw = "".join(f"{service_chars.release_indicator}{c}" if c in reserved else c for c in self.content)
        return self._apply_style(raw, target, style)
