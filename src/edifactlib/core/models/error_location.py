from pydantic import BaseModel

from .interchange import Component, DataElement, FunctionalGroup, Message, Segment


class ErrorLocation(BaseModel):
    functional_group: FunctionalGroup | None = None
    message: Message | None = None
    segment: Segment | None = None
    data_element: DataElement | None = None
    component: Component | None = None
