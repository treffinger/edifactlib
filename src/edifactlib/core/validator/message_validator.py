from ..directory import Directory
from ..exceptions import MessageValidationError
from ..models.interchange import Message, Segment
from ..syntax import Syntax
from .segment_validator import SegmentValidator


class MessageValidator:
    def __init__(self, syntax: Syntax, directory: Directory) -> None:
        self._segment_validator = SegmentValidator(syntax, directory)

    def validate(self, message: Message, version: str, header: Segment, una_seg: Segment | None) -> None:
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
        number_segments = message.trailer.data_elements[0].components[0].content
        if not number_segments:
            raise ValueError("The message could not be validated. Invalid message trailer.")

        try:
            number_segments = int(number_segments)
        except:
            raise MessageValidationError(f"Unable to validate the message. A non-numeric segment count was specified")

        # +2 to include header and trailer segment
        if len(message.segments) + 2 != number_segments:
            raise MessageValidationError(
                f"Unable to validate the message. Segment count does not match. Expected count: {number_segments}, actual count: {len(message.segments) + 2}"
            )

    def _validate_reference_number(self, header: Segment, trailer: Segment) -> None:
        if trailer.data_elements[1].components[0].content != header.data_elements[0].components[0].content:
            raise MessageValidationError("Unable to validate the message. Invalid reference number provided.")
