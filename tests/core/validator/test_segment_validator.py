# ---------------------------------------------------------------------------
# AI-generated: This code (or parts of it) was created with the assistance
# of AI (Claude) and has been reviewed/adapted.
# ---------------------------------------------------------------------------

import pytest

from edifactlib.core.directory import Directory
from edifactlib.core.exceptions import EdifactError, SegmentValidationError
from edifactlib.core.models.interchange import Component, DataElement, Segment
from edifactlib.core.syntax import Syntax
from edifactlib.core.validator.segment_validator import SegmentValidator


def _header(charset_level: str = "UNOC") -> Segment:
    return Segment(
        tag="UNB",
        data_elements=[DataElement(components=[Component(content=charset_level), Component(content="3")], position=0)],
    )


@pytest.fixture
def validator() -> SegmentValidator:
    return SegmentValidator(Syntax(), Directory())


def test_valid_segment_passes(validator):
    nad = Segment(tag="NAD", data_elements=[DataElement(components=[Component(content="BY")], position=0)])

    validator.validate(nad, "3", "D.24A", _header(), None)


def test_missing_required_data_element_raises(validator):
    nad = Segment(tag="NAD", data_elements=[])

    with pytest.raises(SegmentValidationError):
        validator.validate(nad, "3", "D.24A", _header(), None)


def test_data_element_exceeding_max_repeat_raises(validator):
    nad = Segment(
        tag="NAD",
        data_elements=[
            DataElement(components=[Component(content="BY")], position=0),
            DataElement(components=[Component(content="SU")], position=0),
        ],
    )

    with pytest.raises(SegmentValidationError):
        validator.validate(nad, "3", "D.24A", _header(), None)


def test_dir_name_none_uses_syntax_catalog_instead_of_directory(validator):
    unh = Segment(
        tag="UNH",
        data_elements=[
            DataElement(components=[Component(content="1")], position=0),
            DataElement(
                components=[
                    Component(content="ORDERS"),
                    Component(content="D"),
                    Component(content="24A"),
                    Component(content="UN"),
                ],
                position=1,
            ),
        ],
    )

    validator.validate(unh, "3", None, _header(), None)


def test_unknown_segment_tag(validator):
    unknown = Segment(tag="ZZZ", data_elements=[])

    with pytest.raises(SegmentValidationError):
        validator.validate(unknown, "3", "D.24A", _header(), None)


def test_required_data_element_present_but_empty(validator):
    nad = Segment(tag="NAD", data_elements=[DataElement(components=[], position=0)])

    with pytest.raises(EdifactError):
        validator.validate(nad, "3", "D.24A", _header(), None)
