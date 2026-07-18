from pydantic import BaseModel

from .component import Component


class DataElement(BaseModel):
    components: list[Component]
    position: int
    name: str | None = None
