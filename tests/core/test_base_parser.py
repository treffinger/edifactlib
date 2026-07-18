# ---------------------------------------------------------------------------
# AI-generated: This code (or parts of it) was created with the assistance
# of AI (Claude) and has been reviewed/adapted.
# ---------------------------------------------------------------------------

import pytest

from edifactlib.core.exceptions import ParsingError
from edifactlib.core.parser.base_parser import BaseParser


def test_segment_and_data_element_positions(valid_edifact_message):
    interchange = BaseParser().parse(valid_edifact_message)

    bgm = interchange.messages[0].segments[0]
    assert bgm.tag == "BGM"
    assert [de.position for de in bgm.data_elements] == [0, 1, 2]
    assert bgm.data_elements[0].components[0].content == "220"
    assert bgm.data_elements[1].components[0].content == "PO123456"


def test_release_indicator_escapes_delimiters_without_splitting():
    msg = "UNB+x'UNH+1+ORDERS:D:24A:UN'FTX+AAA+++Escaped?+plus and?'quote'UNT+2+1'UNZ+1+x'"

    interchange = BaseParser().parse(msg)

    ftx = interchange.messages[0].segments[0]
    assert ftx.tag == "FTX"
    last_element = ftx.data_elements[-1]
    assert last_element.components[0].content == "Escaped+plus and'quote"


def test_empty_components_are_dropped():
    msg = "UNB+x'UNH+1+ORDERS:D:24A:UN'FTX+AAA+++hello'UNT+2+1'UNZ+1+x'"

    interchange = BaseParser().parse(msg)

    ftx = interchange.messages[0].segments[0]
    # positions 1 and 2 are empty ("+++") and should contain no components at all
    assert ftx.data_elements[1].components == []
    assert ftx.data_elements[2].components == []


def test_unh_segments_are_grouped_into_messages():
    msg = "UNB+x'UNH+1+ORDERS:D:24A:UN'FTX+a'UNT+2+1'UNZ+1+x'"

    interchange = BaseParser().parse(msg)

    assert len(interchange.messages) == 1
    message = interchange.messages[0]
    assert message.header.tag == "UNH"
    assert message.trailer.tag == "UNT"
    assert [s.tag for s in message.segments] == ["FTX"]


def test_ung_segments_are_grouped_into_functional_groups():
    msg = (
        "UNB+x'"
        "UNG+ORDERS+SENDER+RECEIVER+260704:1200+1+UN'"
        "UNH+1+ORDERS:D:24A:UN'FTX+hello'UNT+2+1'"
        "UNH+2+ORDERS:D:24A:UN'FTX+world'UNT+2+2'"
        "UNE+2+1'"
        "UNZ+1+x'"
    )

    interchange = BaseParser().parse(msg)

    assert interchange.messages == []
    assert len(interchange.functional_groups) == 1
    fg = interchange.functional_groups[0]
    assert fg.header.tag == "UNG"
    assert fg.trailer.tag == "UNE"
    assert len(fg.messages) == 2


def test_fewer_than_four_segments_raises_parsing_error():
    with pytest.raises(ParsingError):
        BaseParser().parse("UNB+x'UNZ+1+x'")


def test_unknown_tag_before_unh_or_ung_raises_parsing_error():
    with pytest.raises(ParsingError):
        BaseParser().parse("UNB+x'ZZZ+1'FOO+1'UNZ+1+x'")


def test_unclosed_unh_raises_parsing_error():
    with pytest.raises(ParsingError):
        BaseParser().parse("UNB+x'UNH+1+ORDERS:D:24A:UN'FTX+a'UNZ+1+x'")


def test_missing_unz_raises_parsing_error():
    with pytest.raises(ParsingError):
        BaseParser().parse("UNB+x'UNH+1+ORDERS:D:24A:UN'UNT+2+1'")


def test_line_breaks_are_stripped_before_parsing():
    msg = "UNB+x\r\n'UNH+1+ORDERS:D:24A:UN'\nUNT+2+1'\r\nUNZ+1+x'"

    interchange = BaseParser().parse(msg)

    assert interchange.header.tag == "UNB"
    assert interchange.trailer.tag == "UNZ"
