from pydantic import BaseModel


class ComponentRef(BaseModel):
    tag: str
    required: bool
