from pydantic import BaseModel

from .data_element import DataElement


class Segment(BaseModel):
    tag: str
    data_elements: list[DataElement]
    name: str | None = None
