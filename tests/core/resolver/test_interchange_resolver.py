# ---------------------------------------------------------------------------
# AI-generated: This code (or parts of it) was created with the assistance
# of AI (Claude) and has been reviewed/adapted.
# ---------------------------------------------------------------------------

import pytest

from edifactlib.core.exceptions import EdifactError
from edifactlib.core.parser.base_parser import BaseParser
from edifactlib.core.resolver.interchange_resolver import InterchangeResolver


@pytest.fixture
def resolver() -> InterchangeResolver:
    return InterchangeResolver()


def test_resolves_header_trailer_and_message_segments(resolver, valid_edifact_message):
    interchange = BaseParser().parse(valid_edifact_message)

    resolver.resolve(interchange)

    assert interchange.header.name == "Interchange header"
    assert interchange.trailer.name == "Interchange Trailer"
    assert interchange.messages[0].segments[0].name == "Beginning of message"


def test_resolves_messages_within_functional_groups(resolver):
    msg = (
        "UNB+UNOC:3+SENDER+RECEIVER+260704:1200+REF1'"
        "UNG+ORDERS+SENDER+RECEIVER+260704:1200+1+UN'"
        "UNH+1+ORDERS:D:24A:UN'BGM+220+PO1+9'UNT+2+1'"
        "UNE+1+1'"
        "UNZ+1+REF1'"
    )
    interchange = BaseParser().parse(msg)

    resolver.resolve(interchange)

    fg_message = interchange.functional_groups[0].messages[0]
    assert fg_message.segments[0].name == "Beginning of message"


def test_missing_syntax_version_raises_edifact_error(resolver, valid_edifact_message):
    interchange = BaseParser().parse(valid_edifact_message)
    interchange.header.data_elements[0].components[1].content = None

    with pytest.raises(EdifactError):
        resolver.resolve(interchange)
