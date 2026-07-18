from ..directory import Directory
from ..exceptions import InterchangeValidationError
from ..models.interchange import Interchange, Segment
from ..syntax import Syntax
from .charset_level import ALLOWED_CHARSETS
from .message_validator import MessageValidator
from .segment_validator import SegmentValidator


class InterchangeValidator:
    def __init__(self) -> None:
        syntax = Syntax()
        directory = Directory()
        self._message_validator = MessageValidator(syntax, directory)
        self._segment_validator = SegmentValidator(syntax, directory)

    def validate(self, interchange: Interchange) -> None:
        version = self._get_version(interchange.header)
        self._validate_interchange_header(interchange.header, version, interchange.una)
        self._validate_interchange_trailer(interchange.trailer, version, interchange.header, interchange.una)
        self._validate_structure(interchange)
        self._validate_charset_level(interchange.header)

        for msg in interchange.messages:
            self._message_validator.validate(msg, version, interchange.header, interchange.una)

        for fg in interchange.functional_groups:
            for msg in fg.messages:
                self._message_validator.validate(msg, version, interchange.header, interchange.una)

    def _validate_interchange_header(self, segment: Segment, version: str, una_seg: Segment | None) -> None:
        if segment.tag != "UNB":
            raise InterchangeValidationError("Invalid interchange header provided.")

        self._segment_validator.validate(segment, version, None, segment, una_seg)

    def _validate_interchange_trailer(
        self, segment: Segment, version: str, header: Segment, una_seg: Segment | None
    ) -> None:
        if segment.tag != "UNZ":
            raise InterchangeValidationError("Invalid interchange trailer provided.")

        self._segment_validator.validate(segment, version, None, header, una_seg)
        if segment.data_elements[1].components[0].content != header.data_elements[4].components[0].content:
            raise InterchangeValidationError("Interchange control does not match.")

    def _validate_structure(self, interchange: Interchange) -> None:
        if not interchange.messages and not interchange.functional_groups:
            raise InterchangeValidationError("The interchange does not contain any messages or functional groups.")

        if len(interchange.messages) > 0 and len(interchange.functional_groups) > 0:
            raise InterchangeValidationError(
                "The interchange contains both messages outside of functional groups and functional groups."
            )

    def _validate_charset_level(self, header: Segment) -> None:
        syntax_version = self._get_version(header)
        level = header.data_elements[0].components[0].content
        charsets = ALLOWED_CHARSETS.get(syntax_version, [])
        if level not in charsets:
            raise InterchangeValidationError(
                "The charset specified by the interchange does not match the allowed charsets for this version."
            )

    def _get_version(self, header: Segment) -> str:
        try:
            version = header.data_elements[0].components[1].content
        except IndexError:
            raise InterchangeValidationError("The syntax version of the interchange could not be read.")

        if not version:
            raise InterchangeValidationError("The syntax version of the interchange could not be read.")

        return version
