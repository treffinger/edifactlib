import re

from ..exceptions import DataElementValidationError
from ..models.interchange import Component, Segment
from ..models.syntax import ElementDef
from .charset import LEVEL_ALPHA_FRAGMENTS, LEVEL_FULL_FRAGMENTS


class ComponentValidator:
    def validate(self, component: Component, element_def: ElementDef, header: Segment, una_seg: Segment | None) -> None:
        """Validate the content of a single component against its element definition.

        Checks the length of the content and, depending on the charset
        specified in the element definition (alphabetic, numeric, or
        alphanumeric), whether it contains only allowed characters. For
        numeric values, the decimal separator defined in the UNA segment is
        taken into account. If the content is empty, validation is skipped.

        Args:
            component: The component to validate.
            element_def: The element definition with length and charset
                constraints.
            header: The interchange header segment (UNB) from which the
                charset level is read.
            una_seg: The UNA segment of the message, if present, used to
                determine the decimal separator; otherwise None (default ".").

        Raises:
            DataElementValidationError: If the content's length is outside
                the allowed min/max length, the UNA segment is invalid (too
                short), the charset level is unknown, or the content contains
                characters not allowed for the defined charset.
        """
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
