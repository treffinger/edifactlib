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
    ) -> str:
        """Serialize this part back into raw EDIFACT text.

        Reserved characters in component contents are escaped with the
        release indicator. Segments are placed on separate lines for
        readability.

        Args:
            service_chars: The service characters to use. If None, the
                default service characters are used.
            target: A part of this model whose raw text should be passed
                to ``style``.
            style: A function that receives the raw text of ``target`` and
                returns a styled version of it, e.g. wrapped in ANSI color
                codes. If None, no styling is applied.

        Returns:
            The raw EDIFACT text of this part.
        """

    def _apply_style(self, raw: str, target: InterchangeBaseModel | None, style: Callable | None) -> str:
        return style(raw) if style is not None and self is target else raw
