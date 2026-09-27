# ---------------------------------------------------------------------------
# AI-generated: This code (or parts of it) was created with the assistance
# of AI (Claude) and has been reviewed/adapted.
# ---------------------------------------------------------------------------

import pytest

from edifactlib import Parser
from edifactlib.core.exceptions import DataElementError, EdifactError, InterchangeError, MessageError, SegmentError
from edifactlib.core.models.interchange import Interchange
from edifactlib.core.parser.base_parser import BaseParser
from edifactlib.core.validator.interchange_validator import InterchangeValidator


def _validate(interchange: Interchange) -> EdifactError:
    with pytest.raises(EdifactError) as exc_info:
        InterchangeValidator().validate(interchange)
    return exc_info.value


def test_component_error_is_enriched_on_every_level(valid_edifact_message):
    too_long = "X" * 36  # 3039 (Party identifier) allows at most 35 characters
    interchange = BaseParser().parse(
        valid_edifact_message.replace("NAD+BY+5412345000013::9'", f"NAD+BY+{too_long}::9'")
    )
    nad = interchange.messages[0].segments[2]

    error = _validate(interchange)

    assert isinstance(error, DataElementError)
    assert error.details.interchange is interchange
    assert error.details.segment is nad
    assert error.details.data_element is nad.data_elements[1]
    assert error.details.component is nad.data_elements[1].components[0]


def test_segment_error_has_segment_and_interchange_but_no_data_element(valid_edifact_message):
    interchange = BaseParser().parse(valid_edifact_message.replace("BGM+220+PO123456+9'", "ZZZ+1'"))
    zzz = interchange.messages[0].segments[0]

    error = _validate(interchange)

    assert isinstance(error, SegmentError)
    assert error.details.interchange is interchange
    assert error.details.segment is zzz
    assert error.details.data_element is None
    assert error.details.component is None


def test_message_error_points_to_segment_count(valid_edifact_message):
    interchange = BaseParser().parse(valid_edifact_message.replace("UNT+11+1'", "UNT+99+1'"))
    trailer = interchange.messages[0].trailer

    error = _validate(interchange)

    assert isinstance(error, MessageError)
    assert error.details.interchange is interchange
    assert error.details.component is trailer.data_elements[0].components[0]


def test_interchange_error_points_to_control_reference(valid_edifact_message):
    interchange = BaseParser().parse(valid_edifact_message.replace("UNZ+1+REF00001'", "UNZ+1+OTHER'"))

    error = _validate(interchange)

    assert isinstance(error, InterchangeError)
    assert error.details.interchange is interchange
    assert error.details.component is interchange.trailer.data_elements[1].components[0]


def test_structure_error_has_interchange_but_no_target(valid_edifact_message):
    interchange = BaseParser().parse(valid_edifact_message)
    interchange.messages = []

    error = _validate(interchange)

    assert isinstance(error, InterchangeError)
    assert error.details.interchange is interchange
    assert error.details.segment is None
    assert error.details.data_element is None
    assert error.details.component is None
    assert str(error) == error.message


def test_parser_error_message_highlights_faulty_part(valid_edifact_message):
    with pytest.raises(MessageError) as exc_info:
        Parser().parse(valid_edifact_message.replace("UNT+11+1'", "UNT+99+1'"))

    assert "UNT+\033[31m99\033[0m+1'" in str(exc_info.value)
