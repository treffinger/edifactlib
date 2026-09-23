import re

from ..exceptions import DataElementError
from ..models import ErrorDetails
from ..models.interchange import Component, Segment
from ..models.syntax import ElementDef
from .charset import LEVEL_ALPHA_FRAGMENTS, LEVEL_FULL_FRAGMENTS


class ComponentValidator:
    def validate(
        self, component: Component, required: bool, element_def: ElementDef, header: Segment, una_seg: Segment | None
    ) -> None:
        """Validate the content of a single component against its element definition.

        Checks the length of the content and, depending on the charset
        specified in the element definition (alphabetic, numeric, or
        alphanumeric), whether it contains only allowed characters. For
        numeric values, the decimal separator defined in the UNA segment is
        taken into account. If the content is empty, validation is skipped.

        Args:
            component: The component to validate.
            required: Whether the component is required by its data element
                or composite definition. If True and the content is empty,
                validation fails immediately.
            element_def: The element definition with length and charset
                constraints.
            header: The interchange header segment (UNB) from which the
                charset level is read.
            una_seg: The UNA segment of the message, if present, used to
                determine the decimal separator; otherwise None (default ".").

        Raises:
            DataElementError: If the component is required but its content
                is empty, the content's length is outside the allowed
                min/max length, the UNA segment is invalid (too short), the
                charset level is unknown, or the content contains characters
                not allowed for the defined charset.
        """
        if required and not component.content:
            raise DataElementError(
                f'A component in the data element "{element_def.tag}" is missing.',
                details=ErrorDetails(component=component),
            )

        if not component.content:
            return

        if len(component.content) < element_def.min_length or len(component.content) > element_def.max_length:
            raise DataElementError(
                f"The data element {element_def.tag} has an invalid length. Minimum length: {element_def.min_length}, maximum length: {element_def.max_length}, actual length: {len(component.content)}",
                ErrorDetails(component=component),
            )

        decimal_sep = "."
        if una_seg is not None:
            content = una_seg.data_elements[0].components[0].content
            if not content or len(content) < 3:
                raise DataElementError(
                    "Error validating the component. Invalid UNA segment.", ErrorDetails(component=component)
                )
            decimal_sep = content[2]

        charset_level = str(header.data_elements[0].components[0].content)
        match element_def.charset:
            case "a":
                allowed = self._get_charset_regex(charset_level, "a", component)
                if re.search(rf"[^{allowed}]", component.content):
                    self._raise(element_def, component)
            case "n":
                if re.search(rf"[^0-9\-{re.escape(decimal_sep)}]", component.content):
                    self._raise(element_def, component)
            case "an":
                allowed = self._get_charset_regex(charset_level, "an", component)
                if re.search(rf"[^{allowed}]", component.content):
                    self._raise(element_def, component)

    def _get_charset_regex(self, charset_level: str, charset: str, component: Component) -> str:
        fragments = LEVEL_ALPHA_FRAGMENTS if charset == "a" else LEVEL_FULL_FRAGMENTS
        try:
            return fragments[charset_level]
        except KeyError:
            raise DataElementError("Invalid character set provided.", ErrorDetails(component=component))

    def _raise(self, element_def: ElementDef, component: Component) -> None:
        raise DataElementError(
            f"The data element {element_def.tag} or one of its components contains invalid characters. Allowed charset: {element_def.charset}",
            ErrorDetails(component=component),
        )
