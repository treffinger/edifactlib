# ---------------------------------------------------------------------------
# AI-generated: This code (or parts of it) was created with the assistance
# of AI (Claude) and has been reviewed/adapted.
# ---------------------------------------------------------------------------

import pytest

from edifactlib.core.directory import Directory
from edifactlib.core.models.interchange import Component, DataElement, Message, Segment
from edifactlib.core.parser.base_parser import BaseParser
from edifactlib.core.resolver.message_resolver import MessageResolver
from edifactlib.core.syntax import Syntax


@pytest.fixture
def resolver() -> MessageResolver:
    return MessageResolver(Syntax(), Directory())


def test_resolves_all_segments_in_a_message(resolver, valid_edifact_message):
    interchange = BaseParser().parse(valid_edifact_message)
    message = interchange.messages[0]

    resolver.resolve(message, "3")

    names = {segment.tag: segment.name for segment in message.segments}
    assert names["BGM"] == "Beginning of message"
    assert names["NAD"] == "Name and address"
    assert names["UNS"] == "Section Control"


def test_uns_segment_is_resolved_against_syntax_not_directory(resolver):
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

    resolver.resolve(message, "3")

    assert uns.name == "Section Control"
