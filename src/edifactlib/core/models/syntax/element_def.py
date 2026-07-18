from typing import Literal

from pydantic import BaseModel


class ElementDef(BaseModel):
    tag: str
    name: str
    charset: Literal["a", "n", "an"]
    min_length: int
    max_length: int
