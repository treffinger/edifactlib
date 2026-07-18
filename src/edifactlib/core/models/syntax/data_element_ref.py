from typing import Literal

from pydantic import BaseModel


class DataElementRef(BaseModel):
    tag: str
    type: Literal["EDCD", "EDED"]
    required: bool
    max_repeat: int
