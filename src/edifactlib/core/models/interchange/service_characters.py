from __future__ import annotations

from pydantic import BaseModel

from .segment import Segment


class ServiceCharacters(BaseModel):
    component_sep: str = ":"
    data_element_sep: str = "+"
    decimal_notation: str = "."
    release_indicator: str = "?"
    segment_terminator: str = "'"

    @classmethod
    def from_una(cls, una: Segment) -> ServiceCharacters:
        una_str = una.data_elements[0].components[0].content
        if not una_str or len(una_str) < 6:
            return cls()

        return cls(
            component_sep=una_str[0],
            data_element_sep=una_str[1],
            decimal_notation=una_str[2],
            release_indicator=una_str[3],
            segment_terminator=una_str[5],
        )
