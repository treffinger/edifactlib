import re

from ..exceptions import DataElementValidationError
from ..models.interchange import Component, Segment
from ..models.syntax import ElementDef
from .charset import LEVEL_ALPHA_FRAGMENTS, LEVEL_FULL_FRAGMENTS


class ComponentValidator:
    def validate(self, component: Component, element_def: ElementDef, header: Segment, una_seg: Segment | None) -> None:
        if not component.content:
            return

        if len(component.content) < element_def.min_length or len(component.content) > element_def.max_length:
            raise DataElementValidationError(
                f"The data element {element_def.tag} has an invalid length. Minimum length: {element_def.min_length}, maximum length: {element_def.max_length}, actual length: {len(component.content)}"
            )

        decimal_sep = "."
        if una_seg is not None:
            content = una_seg.data_elements[0].components[0].content
            if not content or len(content) < 3:
                raise DataElementValidationError("Error validating the component. Invalid UNA segment.")
            decimal_sep = content[2]

        charset_level = str(header.data_elements[0].components[0].content)
        match element_def.charset:
            case "a":
                allowed = self._get_charset_regex(charset_level, "a")
                if re.search(rf"[^{allowed}]", component.content):
                    self._raise(element_def)
            case "n":
                if re.search(rf"[^0-9\-{re.escape(decimal_sep)}]", component.content):
                    self._raise(element_def)
            case "an":
                allowed = self._get_charset_regex(charset_level, "an")
                if re.search(rf"[^{allowed}]", component.content):
                    self._raise(element_def)

    def _get_charset_regex(self, charset_level: str, charset: str) -> str:
        fragments = LEVEL_ALPHA_FRAGMENTS if charset == "a" else LEVEL_FULL_FRAGMENTS
        try:
            return fragments[charset_level]
        except KeyError:
            raise DataElementValidationError("Invalid character set provided.")

    def _raise(self, element_def: ElementDef) -> None:
        raise DataElementValidationError(
            f"The data element {element_def.tag} or one of its components contains invalid characters. Allowed charset: {element_def.charset}"
        )
