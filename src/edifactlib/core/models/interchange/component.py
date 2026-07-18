from pydantic import BaseModel


class Component(BaseModel):
    content: str | None
    name: str | None = None
