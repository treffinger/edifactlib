# ---------------------------------------------------------------------------
# AI-generated: This code (or parts of it) was created with the assistance
# of AI (Claude) and has been reviewed/adapted.
# ---------------------------------------------------------------------------

import pytest

from edifactlib.core.models.interchange import Component, DataElement, Segment, ServiceCharacters


def _una(content: str | None) -> Segment:
    return Segment(tag="UNA", data_elements=[DataElement(components=[Component(content=content)], position=0)])


def test_defaults_are_standard_service_characters():
    chars = ServiceCharacters()

    assert chars.component_sep == ":"
    assert chars.data_element_sep == "+"
    assert chars.decimal_notation == "."
    assert chars.release_indicator == "?"
    assert chars.segment_terminator == "'"


def test_from_una_reads_custom_service_characters():
    chars = ServiceCharacters.from_una(_una("|*,! ~"))

    assert chars.component_sep == "|"
    assert chars.data_element_sep == "*"
    assert chars.decimal_notation == ","
    assert chars.release_indicator == "!"
    assert chars.segment_terminator == "~"


@pytest.mark.parametrize("content", [None, "", ":+.? "])
def test_from_una_falls_back_to_defaults_for_missing_or_too_short_content(content):
    assert ServiceCharacters.from_una(_una(content)) == ServiceCharacters()
