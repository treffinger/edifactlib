from pydantic import BaseModel

from .component_ref import ComponentRef


class CompositeDef(BaseModel):
    tag: str
    name: str
    components: list[ComponentRef]
