from __future__ import annotations

from abc import abstractmethod
from typing import Callable

from pydantic import BaseModel

from .service_characters import ServiceCharacters


class InterchangeBaseModel(BaseModel):
    @abstractmethod
    def dump_raw(
        self,
        service_chars: ServiceCharacters | None = None,
        target: InterchangeBaseModel | None = None,
        style: Callable | None = None,
    ) -> str: ...

    def _apply_style(self, raw: str, target: InterchangeBaseModel | None, style: Callable | None) -> str:
        return style(raw) if style is not None and self is target else raw
