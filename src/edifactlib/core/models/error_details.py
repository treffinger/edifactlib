from pydantic import BaseModel

from .interchange import Component, DataElement, Interchange, Segment


class ErrorDetails(BaseModel):
    interchange: Interchange | None = None
    segment: Segment | None = None
    data_element: DataElement | None = None
    component: Component | None = None
