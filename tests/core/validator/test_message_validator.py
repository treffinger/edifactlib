# ---------------------------------------------------------------------------
# AI-generated: This code (or parts of it) was created with the assistance
# of AI (Claude) and has been reviewed/adapted.
# ---------------------------------------------------------------------------

import pytest

from edifactlib.core.directory import Directory
from edifactlib.core.exceptions import MessageValidationError
from edifactlib.core.models.interchange import Component, DataElement, Message, Segment
from edifactlib.core.parser.base_parser import BaseParser
from edifactlib.core.syntax import Syntax
from edifactlib.core.validator.message_validator import MessageValidator


@pytest.fixture
def validator() -> MessageValidator:
    return MessageValidator(Syntax(), Directory())


@pytest.fixture
def parsed(valid_edifact_message):
    return BaseParser().parse(valid_edifact_message)


def test_valid_message_passes(validator, parsed):
    message = parsed.messages[0]

    validator.validate(message, "3", parsed.header, parsed.una)


def test_segment_count_mismatch_raises(validator, parsed):
    message = parsed.messages[0]
    message.trailer.data_elements[0].components[0].content = "99"

    with pytest.raises(MessageValidationError):
        validator.validate(message, "3", parsed.header, parsed.una)


def test_reference_number_mismatch_raises(validator, parsed):
    message = parsed.messages[0]
    message.trailer.data_elements[1].components[0].content = "999"

    with pytest.raises(MessageValidationError):
        validator.validate(message, "3", parsed.header, parsed.una)


def test_non_numeric_segment_count(validator, parsed):
    message = parsed.messages[0]
    message.trailer.data_elements[0].components[0].content = "ABC"

    with pytest.raises(MessageValidationError):
        validator.validate(message, "3", parsed.header, parsed.una)


def test_uns_segment_is_validated_against_syntax_not_directory(validator):
    """UNS/TXT segments are validated against the Syntax catalog regardless of the
    message's directory version, so an unresolvable dir_name (here "D.99Z", derived
    from the message identifier) must not stop a UNS segment from validating.
    """
    header = Segment(
        tag="UNH",
        data_elements=[
            DataElement(components=[Component(content="1")], position=0),
            DataElement(
                components=[
                    Component(content="ORDERS"),
                    Component(content="D"),
                    Component(content="99Z"),
                    Component(content="UN"),
                ],
                position=1,
            ),
        ],
    )
    trailer = Segment(
        tag="UNT",
        data_elements=[
            DataElement(components=[Component(content="3")], position=0),
            DataElement(components=[Component(content="1")], position=1),
        ],
    )
    uns = Segment(tag="UNS", data_elements=[DataElement(components=[Component(content="S")], position=0)])
    message = Message(header=header, trailer=trailer, segments=[uns])

    interchange_header = Segment(
        tag="UNB",
        data_elements=[DataElement(components=[Component(content="UNOC"), Component(content="3")], position=0)],
    )

    validator.validate(message, "3", interchange_header, None)
