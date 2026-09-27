# ---------------------------------------------------------------------------
# AI-generated: This code (or parts of it) was created with the assistance
# of AI (Claude) and has been reviewed/adapted.
# ---------------------------------------------------------------------------

from edifactlib.core.exceptions import EdifactError
from edifactlib.core.models import ErrorDetails
from edifactlib.core.parser.base_parser import BaseParser

RED = "\033[31m"
RESET = "\033[0m"


def test_details_default_to_empty_error_details():
    error = EdifactError("boom")

    assert error.message == "boom"
    assert error.details == ErrorDetails()


def test_str_without_details_is_plain_message():
    assert str(EdifactError("boom")) == "boom"


def test_str_with_target_but_without_interchange_is_plain_message(valid_edifact_message):
    interchange = BaseParser().parse(valid_edifact_message)

    error = EdifactError("boom", ErrorDetails(segment=interchange.header))

    assert str(error) == "boom"


def test_str_with_interchange_but_without_target_is_plain_message(valid_edifact_message):
    interchange = BaseParser().parse(valid_edifact_message)

    error = EdifactError("boom", ErrorDetails(interchange=interchange))

    assert str(error) == "boom"


def test_str_highlights_faulty_component_in_interchange(valid_edifact_message):
    interchange = BaseParser().parse(valid_edifact_message)
    component = interchange.messages[0].trailer.data_elements[0].components[0]

    error = EdifactError("boom", ErrorDetails(interchange=interchange, component=component))

    assert str(error).startswith("boom\n\nFaulty part:\n")
    assert f"UNT+{RED}11{RESET}+1'" in str(error)


def test_str_prefers_most_specific_target(valid_edifact_message):
    interchange = BaseParser().parse(valid_edifact_message)
    segment = interchange.messages[0].trailer
    data_element = segment.data_elements[0]
    component = data_element.components[0]

    error = EdifactError(
        "boom", ErrorDetails(interchange=interchange, segment=segment, data_element=data_element, component=component)
    )

    assert str(error).count(RED) == 1
    assert f"UNT+{RED}11{RESET}+1'" in str(error)


def test_str_falls_back_to_segment_target(valid_edifact_message):
    interchange = BaseParser().parse(valid_edifact_message)
    segment = interchange.messages[0].segments[0]

    error = EdifactError("boom", ErrorDetails(interchange=interchange, segment=segment))

    assert f"{RED}BGM+220+PO123456+9{RESET}'" in str(error)
