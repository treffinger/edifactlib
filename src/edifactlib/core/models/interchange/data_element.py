from typing import Callable, override

from .component import Component
from .interchange_base_model import InterchangeBaseModel
from .service_characters import ServiceCharacters


class DataElement(InterchangeBaseModel):
    components: list[Component]
    position: int
    name: str | None = None

    @override
    def dump_raw(
        self,
        service_chars: ServiceCharacters | None = None,
        target: InterchangeBaseModel | None = None,
        style: Callable | None = None,
    ) -> str:
        service_chars = service_chars or ServiceCharacters()
        raw = service_chars.component_sep.join(
            [component.dump_raw(service_chars, target, style) for component in self.components]
        )
        return self._apply_style(raw, target, style)
