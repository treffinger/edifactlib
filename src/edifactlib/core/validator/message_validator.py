from ..directory import Directory
from ..exceptions import MessageError
from ..models import ErrorDetails
from ..models.interchange import Message, Segment
from ..syntax import Syntax
from .segment_validator import SegmentValidator


class MessageValidator:
    def __init__(self, syntax: Syntax, directory: Directory) -> None:
        self._segment_validator = SegmentValidator(syntax, directory)

    def validate(self, message: Message, version: str, header: Segment, una_seg: Segment | None) -> None:
        """Validate a single message.

        Checks the segment count stated in the trailer against the actual
        count, as well as the reference number matching between the header
        and trailer. Then validates all segments of the message, where UNS
        and TXT are validated generically (without a directory), since they
        are not part of the message-specific definition.

        Args:
            message: The message to validate.
            version: The syntax version of the message.
            header: The interchange header segment (UNB), passed through to
                subordinate validators for charset validation.
            una_seg: The UNA segment of the message, if present, otherwise
                None.

        Raises:
            MessageError: If the trailer does not contain a segment
                count, the segment count is not numeric, does not match the
                actual number of segments, or the reference number of header
                and trailer does not match.
            SegmentError: If a segment of the message cannot be
                found or violates its definition.
            DataElementError: If a data element or component of a
                segment of the message is invalid.
        """
        self._validate_segment_count(message)
        self._validate_reference_number(message.header, message.trailer)

        msg_identifier = message.header.data_elements[1]
        dir_name = f"{msg_identifier.components[1].content}.{msg_identifier.components[2].content}"
        for segment in message.segments:
            if segment.tag == "UNS" or segment.tag == "TXT":
                self._segment_validator.validate(segment, version, None, header, una_seg)
            else:
                self._segment_validator.validate(segment, version, dir_name, header, una_seg)

    def _validate_segment_count(self, message: Message) -> None:
        segment_comp = message.trailer.data_elements[0].components[0]
        if not segment_comp.content:
            raise MessageError(
                "The message could not be validated. Invalid message trailer.",
                details=ErrorDetails(component=segment_comp),
            )

        try:
            number_segments = int(segment_comp.content)
        except:
            raise MessageError(
                f"Unable to validate the message. A non-numeric segment count was specified",
                details=ErrorDetails(component=segment_comp),
            )

        # +2 to include header and trailer segment
        if len(message.segments) + 2 != number_segments:
            raise MessageError(
                f"Unable to validate the message. Segment count does not match. Expected count: {number_segments}, actual count: {len(message.segments) + 2}",
                details=ErrorDetails(component=segment_comp),
            )

    def _validate_reference_number(self, header: Segment, trailer: Segment) -> None:
        if trailer.data_elements[1].components[0].content != header.data_elements[0].components[0].content:
            raise MessageError(
                "Unable to validate the message. Invalid reference number provided.",
                details=ErrorDetails(component=trailer.data_elements[1].components[0]),
            )
