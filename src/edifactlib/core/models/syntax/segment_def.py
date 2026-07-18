from pydantic import BaseModel

from .data_element_ref import DataElementRef


class SegmentDef(BaseModel):
    tag: str
    name: str
    data_elements: list[DataElementRef]
