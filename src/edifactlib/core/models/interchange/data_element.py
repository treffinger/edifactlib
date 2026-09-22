from __future__ import annotations

from typing import TYPE_CHECKING, Callable, override

from .component import Component
from .interchange_base_model import InterchangeBaseModel

if TYPE_CHECKING:
    from .service_characters import ServiceCharacters


class DataElement(InterchangeBaseModel):
    components: list[Component]
    position: int
    name: str | None = None

    @override
    def dump_raw(
        self, service_chars: ServiceCharacters, target: InterchangeBaseModel | None, style: Callable | None
    ) -> str:
        raw = service_chars.component_sep.join(
            [component.dump_raw(service_chars, target, style) for component in self.components]
        )
        return self._apply_style(raw, target, style)
