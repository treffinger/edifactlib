from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel

from .component import Component

if TYPE_CHECKING:
    from .service_characters import ServiceCharacters


class DataElement(BaseModel):
    components: list[Component]
    position: int
    name: str | None = None

    def dump_raw(self, service_chars: ServiceCharacters) -> str:
        raw = service_chars.component_sep.join([component.dump_raw(service_chars) for component in self.components])
        return raw
