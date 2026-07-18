# ---------------------------------------------------------------------------
# AI-generated: This code (or parts of it) was created with the assistance
# of AI (Claude) and has been reviewed/adapted.
# ---------------------------------------------------------------------------

import pytest

from edifactlib import Parser
from edifactlib.core.exceptions import MessageValidationError, ParsingError


def test_parse_valid_message_returns_interchange(valid_edifact_message):
    interchange = Parser().parse(valid_edifact_message)

    assert interchange.header.tag == "UNB"
    assert interchange.trailer.tag == "UNZ"
    assert len(interchange.messages) == 1
    assert interchange.messages[0].header.tag == "UNH"


def test_custom_una_separators_are_respected(valid_edifact_message):
    body = valid_edifact_message.split("\n", 1)[1].replace("'", "|")
    custom_una_msg = "UNA:+.? |\n" + body

    interchange = Parser().parse(custom_una_msg)

    assert interchange.trailer.tag == "UNZ"
    assert len(interchange.messages) == 1


def test_default_separators_without_una_segment(valid_edifact_message):
    no_una_msg = valid_edifact_message.split("\n", 1)[1]

    interchange = Parser().parse(no_una_msg)

    assert interchange.una is None
    assert interchange.header.tag == "UNB"
    assert len(interchange.messages) == 1


def test_syntax_version_2_is_supported(valid_edifact_message):
    v2_msg = valid_edifact_message.replace("UNOC:3", "UNOA:2")

    interchange = Parser().parse(v2_msg)

    assert interchange.header.data_elements[0].components[1].content == "2"


def test_syntax_version_3_is_supported(valid_edifact_message):
    interchange = Parser().parse(valid_edifact_message)

    assert interchange.header.data_elements[0].components[1].content == "3"


def test_unsupported_version_raises_parsing_error(valid_edifact_message):
    invalid_version_msg = valid_edifact_message.replace("UNOC:3", "UNOC:9")

    with pytest.raises(ParsingError):
        Parser().parse(invalid_version_msg)


def test_validate_false_skips_validation(valid_edifact_message):
    bad_count_msg = valid_edifact_message.replace("UNT+11+1'", "UNT+99+1'")

    interchange = Parser().parse(bad_count_msg, validate=False)

    assert interchange.trailer.tag == "UNZ"


def test_validate_true_by_default_raises_on_invalid_structure(valid_edifact_message):
    bad_count_msg = valid_edifact_message.replace("UNT+11+1'", "UNT+99+1'")

    with pytest.raises(MessageValidationError):
        Parser().parse(bad_count_msg)


def test_reused_parser_does_not_leak_separator_state_between_calls(valid_edifact_message):
    """Regression test for the documented state-leak bug (CODE_REVIEW_FOLLOWUP.md, 2.1):

    BaseParser stores its separators as instance state, only ever reset inside
    _handle_custom_una. A Parser instance is reused across calls, so a message with
    custom UNA separators contaminates the separators used for a later, fully
    standard message that has no UNA segment of its own.
    """
    body = valid_edifact_message.split("\n", 1)[1].replace("'", "|")
    custom_una_msg = "UNA:+.? |\n" + body
    no_una_msg = valid_edifact_message.split("\n", 1)[1]

    parser = Parser()
    parser.parse(custom_una_msg)

    interchange = parser.parse(no_una_msg)

    assert interchange.header.tag == "UNB"
