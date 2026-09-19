from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel

from .data_element import DataElement

if TYPE_CHECKING:
    from .service_characters import ServiceCharacters


class Segment(BaseModel):
    tag: str
    data_elements: list[DataElement]
    name: str | None = None

    def dump_raw(self, service_chars: ServiceCharacters) -> str:
        if self.tag == "UNA":
            return f"UNA{service_chars.component_sep}{service_chars.data_element_sep}{service_chars.decimal_notation}{service_chars.release_indicator} {service_chars.segment_terminator}"

        raw = f"{self.tag}{service_chars.data_element_sep}"
        raw += service_chars.data_element_sep.join([element.dump_raw(service_chars) for element in self.data_elements])
        return raw
