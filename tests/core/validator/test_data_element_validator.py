# ---------------------------------------------------------------------------
# AI-generated: This code (or parts of it) was created with the assistance
# of AI (Claude) and has been reviewed/adapted.
# ---------------------------------------------------------------------------

import pytest

from edifactlib.core.directory import Directory
from edifactlib.core.exceptions import DataElementValidationError
from edifactlib.core.models.interchange import Component, DataElement, Segment
from edifactlib.core.models.syntax import DataElementRef
from edifactlib.core.syntax import Syntax
from edifactlib.core.validator.data_element_validator import DataElementValidator


def _header(charset_level: str = "UNOC") -> Segment:
    return Segment(
        tag="UNB",
        data_elements=[DataElement(components=[Component(content=charset_level), Component(content="3")], position=0)],
    )


@pytest.fixture
def validator() -> DataElementValidator:
    return DataElementValidator(Syntax(), Directory())


def test_optional_absent_data_element_is_skipped(validator):
    ref = DataElementRef(tag="1004", type="EDED", required=False, max_repeat=1)
    data_element = DataElement(components=[], position=2)

    validator.validate(data_element, ref, "3", "D.24A", _header(), None)


def test_eded_valid_single_value_passes(validator):
    ref = DataElementRef(tag="1004", type="EDED", required=True, max_repeat=1)
    data_element = DataElement(components=[Component(content="PO123456")], position=1)

    validator.validate(data_element, ref, "3", "D.24A", _header(), None)


def test_eded_required_but_missing_content_raises(validator):
    ref = DataElementRef(tag="1004", type="EDED", required=True, max_repeat=1)
    data_element = DataElement(components=[Component(content=None)], position=1)

    with pytest.raises(DataElementValidationError):
        validator.validate(data_element, ref, "3", "D.24A", _header(), None)


def test_eded_with_multiple_components_raises():
    validator = DataElementValidator(Syntax(), Directory())
    ref = DataElementRef(tag="1004", type="EDED", required=False, max_repeat=1)
    data_element = DataElement(components=[Component(content="A"), Component(content="B")], position=1)

    with pytest.raises(DataElementValidationError):
        validator.validate(data_element, ref, "3", "D.24A", _header(), None)


def test_edcd_with_all_required_subcomponents_passes(validator):
    ref = DataElementRef(tag="C507", type="EDCD", required=True, max_repeat=1)
    data_element = DataElement(components=[Component(content="203")], position=0)

    validator.validate(data_element, ref, "3", "D.24A", _header(), None)


def test_edcd_missing_required_subcomponent_raises(validator):
    ref = DataElementRef(tag="C507", type="EDCD", required=True, max_repeat=1)
    data_element = DataElement(components=[], position=0)

    with pytest.raises(DataElementValidationError):
        validator.validate(data_element, ref, "3", "D.24A", _header(), None)
