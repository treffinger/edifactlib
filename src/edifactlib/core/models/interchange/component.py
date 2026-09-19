from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from .service_characters import ServiceCharacters


class Component(BaseModel):
    content: str | None
    name: str | None = None

    def dump_raw(self, service_chars: ServiceCharacters) -> str:
        if not self.content:
            return ""

        reserved = {
            service_chars.component_sep,
            service_chars.data_element_sep,
            service_chars.segment_terminator,
            service_chars.release_indicator,
        }
        return "".join(f"{service_chars.release_indicator}{c}" if c in reserved else c for c in self.content)
