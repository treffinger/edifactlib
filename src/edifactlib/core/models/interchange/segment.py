from __future__ import annotations

from typing import TYPE_CHECKING, Callable, override

from .data_element import DataElement
from .interchange_base_model import InterchangeBaseModel

if TYPE_CHECKING:
    from .service_characters import ServiceCharacters


class Segment(InterchangeBaseModel):
    tag: str
    data_elements: list[DataElement]
    name: str | None = None

    @override
    def dump_raw(
        self, service_chars: ServiceCharacters, target: InterchangeBaseModel | None, style: Callable | None
    ) -> str:
        if self.tag == "UNA":
            return f"UNA{service_chars.component_sep}{service_chars.data_element_sep}{service_chars.decimal_notation}{service_chars.release_indicator} {service_chars.segment_terminator}"

        raw = f"{self.tag}{service_chars.data_element_sep}"
        raw += service_chars.data_element_sep.join(
            [element.dump_raw(service_chars, target, style) for element in self.data_elements]
        )
        return self._apply_style(raw, target, style)
