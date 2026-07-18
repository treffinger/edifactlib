# ---------------------------------------------------------------------------
# AI-generated: This code (or parts of it) was created with the assistance
# of AI (Claude) and has been reviewed/adapted.
# ---------------------------------------------------------------------------

import pytest

from edifactlib.core.exceptions import DataElementValidationError
from edifactlib.core.models.interchange import Component, DataElement, Segment
from edifactlib.core.models.syntax import ElementDef
from edifactlib.core.validator.component_validator import ComponentValidator


def _header(charset_level: str = "UNOC") -> Segment:
    return Segment(
        tag="UNB",
        data_elements=[DataElement(components=[Component(content=charset_level), Component(content="3")], position=0)],
    )


def _una(content: str = ":+.? ") -> Segment:
    return Segment(tag="UNA", data_elements=[DataElement(components=[Component(content=content)], position=0)])


@pytest.fixture
def validator() -> ComponentValidator:
    return ComponentValidator()


def test_valid_content_within_length_passes(validator):
    element_def = ElementDef(tag="6060", name="Quantity", charset="an", min_length=1, max_length=10)
    component = Component(content="ABC123")

    validator.validate(component, element_def, _header(), None)


def test_content_shorter_than_min_length_raises(validator):
    element_def = ElementDef(tag="6060", name="Quantity", charset="an", min_length=5, max_length=10)
    component = Component(content="AB")

    with pytest.raises(DataElementValidationError):
        validator.validate(component, element_def, _header(), None)


def test_content_longer_than_max_length_raises(validator):
    element_def = ElementDef(tag="1004", name="Document identifier", charset="an", min_length=1, max_length=5)
    component = Component(content="X" * 6)

    with pytest.raises(DataElementValidationError):
        validator.validate(component, element_def, _header(), None)


@pytest.mark.parametrize("content", [None, ""])
def test_empty_or_none_content_is_always_accepted(validator, content):
    element_def = ElementDef(tag="1004", name="Document identifier", charset="n", min_length=1, max_length=5)
    component = Component(content=content)

    validator.validate(component, element_def, _header(), None)


def test_numeric_charset_accepts_digits_minus_and_decimal_separator(validator):
    element_def = ElementDef(tag="6060", name="Quantity", charset="n", min_length=1, max_length=10)
    component = Component(content="-12.5")

    validator.validate(component, element_def, _header(), None)


def test_numeric_charset_rejects_letters(validator):
    element_def = ElementDef(tag="6060", name="Quantity", charset="n", min_length=1, max_length=10)
    component = Component(content="12A")

    with pytest.raises(DataElementValidationError):
        validator.validate(component, element_def, _header(), None)


def test_numeric_charset_uses_custom_decimal_separator_from_una(validator):
    element_def = ElementDef(tag="6060", name="Quantity", charset="n", min_length=1, max_length=10)
    component = Component(content="12,5")

    validator.validate(component, element_def, _header(), _una(":+,? "))


def test_numeric_charset_rejects_foreign_decimal_separator_without_matching_una(validator):
    element_def = ElementDef(tag="6060", name="Quantity", charset="n", min_length=1, max_length=10)
    component = Component(content="12,5")

    with pytest.raises(DataElementValidationError):
        validator.validate(component, element_def, _header(), None)


def test_missing_or_too_short_una_content_raises(validator):
    element_def = ElementDef(tag="6060", name="Quantity", charset="n", min_length=1, max_length=10)
    component = Component(content="12.5")

    with pytest.raises(DataElementValidationError):
        validator.validate(component, element_def, _header(), _una("AB"))


def test_alpha_charset_unoa_rejects_lowercase(validator):
    element_def = ElementDef(tag="3036", name="Party name", charset="a", min_length=1, max_length=10)
    component = Component(content="acme")

    with pytest.raises(DataElementValidationError):
        validator.validate(component, element_def, _header("UNOA"), None)


def test_alpha_charset_unob_accepts_lowercase(validator):
    element_def = ElementDef(tag="3036", name="Party name", charset="a", min_length=1, max_length=10)
    component = Component(content="acme")

    validator.validate(component, element_def, _header("UNOB"), None)


def test_alphanumeric_charset_unoa_rejects_lowercase(validator):
    element_def = ElementDef(tag="3036", name="Party name", charset="an", min_length=1, max_length=10)
    component = Component(content="acme123")

    with pytest.raises(DataElementValidationError):
        validator.validate(component, element_def, _header("UNOA"), None)


def test_alphanumeric_charset_unob_accepts_lowercase_and_digits(validator):
    element_def = ElementDef(tag="3036", name="Party name", charset="an", min_length=1, max_length=10)
    component = Component(content="acme123")

    validator.validate(component, element_def, _header("UNOB"), None)


def test_unknown_charset_level_raises(validator):
    element_def = ElementDef(tag="3036", name="Party name", charset="an", min_length=1, max_length=10)
    component = Component(content="ACME")

    with pytest.raises(DataElementValidationError):
        validator.validate(component, element_def, _header("UNOZ"), None)
