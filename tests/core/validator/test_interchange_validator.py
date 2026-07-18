# ---------------------------------------------------------------------------
# AI-generated: This code (or parts of it) was created with the assistance
# of AI (Claude) and has been reviewed/adapted.
# ---------------------------------------------------------------------------

import pytest

from edifactlib.core.exceptions import InterchangeValidationError
from edifactlib.core.models.interchange import FunctionalGroup, Segment
from edifactlib.core.parser.base_parser import BaseParser
from edifactlib.core.validator.interchange_validator import InterchangeValidator


@pytest.fixture
def validator() -> InterchangeValidator:
    return InterchangeValidator()


@pytest.fixture
def parsed(valid_edifact_message):
    return BaseParser().parse(valid_edifact_message)


def test_valid_interchange_passes(validator, parsed):
    validator.validate(parsed)


def test_header_tag_must_be_unb(validator, parsed):
    parsed.header.tag = "XXX"

    with pytest.raises(InterchangeValidationError):
        validator.validate(parsed)


def test_trailer_tag_must_be_unz(validator, parsed):
    parsed.trailer.tag = "XXX"

    with pytest.raises(InterchangeValidationError):
        validator.validate(parsed)


def test_unb_unz_reference_mismatch_raises(validator, parsed):
    parsed.trailer.data_elements[1].components[0].content = "MISMATCH"

    with pytest.raises(InterchangeValidationError):
        validator.validate(parsed)


def test_no_messages_and_no_functional_groups_raises(validator, parsed):
    parsed.messages = []

    with pytest.raises(InterchangeValidationError):
        validator.validate(parsed)


def test_both_messages_and_functional_groups_raises(validator, parsed):
    parsed.functional_groups = [
        FunctionalGroup(header=Segment(tag="UNG", data_elements=[]), trailer=Segment(tag="UNE", data_elements=[]), messages=[])
    ]

    with pytest.raises(InterchangeValidationError):
        validator.validate(parsed)


def test_disallowed_charset_level_for_syntax_version_raises(validator, parsed):
    # UNOC is only allowed from syntax version 3 onward, not for version 2.
    parsed.header.data_elements[0].components[1].content = "2"

    with pytest.raises(InterchangeValidationError):
        validator.validate(parsed)


def test_missing_syntax_version_raises(validator, parsed):
    parsed.header.data_elements[0].components[1].content = None

    with pytest.raises(InterchangeValidationError):
        validator.validate(parsed)
