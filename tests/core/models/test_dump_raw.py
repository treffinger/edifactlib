# ---------------------------------------------------------------------------
# AI-generated: This code (or parts of it) was created with the assistance
# of AI (Claude) and has been reviewed/adapted.
# ---------------------------------------------------------------------------

import pytest

from edifactlib.core.models.interchange import Component, DataElement, Message, Segment, ServiceCharacters
from edifactlib.core.parser.base_parser import BaseParser


def _mark(text: str) -> str:
    return f"<{text}>"


def _one_line(raw: str) -> str:
    return raw.replace("\n", "")


def test_component_escapes_reserved_characters():
    component = Component(content="a+b:c?d'e.f")

    assert component.dump_raw() == "a?+b?:c??d?'e.f"


def test_component_escapes_custom_service_characters():
    chars = ServiceCharacters(component_sep="|", data_element_sep="*", release_indicator="!", segment_terminator="~")
    component = Component(content="a*b|c!d~e+f")

    assert component.dump_raw(chars) == "a!*b!|c!!d!~e+f"


@pytest.mark.parametrize("content", [None, ""])
def test_empty_component_dumps_to_empty_string(content):
    assert Component(content=content).dump_raw() == ""


def test_data_element_keeps_empty_components():
    element = DataElement(components=[Component(content=None), Component(content="20260704")], position=0)

    assert element.dump_raw() == ":20260704"


def test_segment_joins_data_elements():
    segment = Segment(
        tag="NAD",
        data_elements=[
            DataElement(components=[Component(content="BY")], position=0),
            DataElement(
                components=[Component(content="123"), Component(content=None), Component(content="9")], position=1
            ),
        ],
    )

    assert segment.dump_raw() == "NAD+BY+123::9"


def test_message_puts_each_segment_on_its_own_line():
    msg = "UNB+x'UNH+1+ORDERS:D:24A:UN'BGM+220'DTM+137:20260704:102'UNT+4+1'UNZ+1+x'"
    message = BaseParser().parse(msg).messages[0]

    assert message.dump_raw() == "UNH+1+ORDERS:D:24A:UN'\nBGM+220'\nDTM+137:20260704:102'\nUNT+4+1'"


def test_message_without_segments():
    message = Message(
        header=Segment(tag="UNH", data_elements=[DataElement(components=[Component(content="1")], position=0)]),
        trailer=Segment(tag="UNT", data_elements=[DataElement(components=[Component(content="2")], position=0)]),
        segments=[],
    )

    assert message.dump_raw() == "UNH+1'\nUNT+2'"


def test_interchange_round_trip(valid_edifact_message):
    interchange = BaseParser().parse(valid_edifact_message)

    assert interchange.dump_raw() == valid_edifact_message.strip()


def test_interchange_round_trip_with_release_characters():
    msg = "UNA:+.? 'UNB+UNOC:3+S+R+260101:1200+REF1'UNH+1+ORDERS:D:24A:UN'FTX+AAI+++a?+b?:c??d?'e'UNT+3+1'UNZ+1+REF1'"
    interchange = BaseParser().parse(msg)

    assert _one_line(interchange.dump_raw()) == msg


def test_interchange_round_trip_with_custom_una():
    msg = "UNA|*,! ~UNB*UNOC|3*S*R*260101|1200*REF1~UNH*1*ORDERS|D|24A|UN~FTX*AAI***a!*b!~c~UNT*3*1~UNZ*1*REF1~"
    interchange = BaseParser().parse(msg)

    assert _one_line(interchange.dump_raw()) == msg


def test_interchange_without_una_uses_default_service_characters():
    msg = "UNB+UNOC:3+S+R+260101:1200+REF1'UNH+1+ORDERS:D:24A:UN'BGM+220'UNT+3+1'UNZ+1+REF1'"
    interchange = BaseParser().parse(msg)

    assert _one_line(interchange.dump_raw()) == msg


def test_interchange_without_una_uses_passed_service_characters():
    msg = "UNB+UNOC:3+S+R+260101:1200+REF1'UNH+1+ORDERS:D:24A:UN'BGM+220'UNT+3+1'UNZ+1+REF1'"
    interchange = BaseParser().parse(msg)

    raw = interchange.dump_raw(ServiceCharacters(data_element_sep="*"))

    assert _one_line(raw) == msg.replace("+", "*")


def test_passed_service_characters_take_precedence_over_una():
    msg = "UNA|*,! ~UNB*UNOC|3*S*R*260101|1200*REF1~UNH*1*ORDERS|D|24A|UN~BGM*220~UNT*3*1~UNZ*1*REF1~"
    interchange = BaseParser().parse(msg)

    raw = interchange.dump_raw(ServiceCharacters())

    assert _one_line(raw) == (
        "UNA:+.? 'UNB+UNOC:3+S+R+260101:1200+REF1'UNH+1+ORDERS:D:24A:UN'BGM+220'UNT+3+1'UNZ+1+REF1'"
    )


def test_interchange_puts_multiple_messages_on_separate_lines():
    msg = (
        "UNB+UNOC:3+S+R+260101:1200+REF1'"
        "UNH+1+ORDERS:D:24A:UN'BGM+220'UNT+3+1'"
        "UNH+2+ORDERS:D:24A:UN'BGM+220'UNT+3+2'"
        "UNZ+2+REF1'"
    )
    interchange = BaseParser().parse(msg)

    assert interchange.dump_raw().splitlines() == [
        "UNB+UNOC:3+S+R+260101:1200+REF1'",
        "UNH+1+ORDERS:D:24A:UN'",
        "BGM+220'",
        "UNT+3+1'",
        "UNH+2+ORDERS:D:24A:UN'",
        "BGM+220'",
        "UNT+3+2'",
        "UNZ+2+REF1'",
    ]


def test_interchange_round_trip_with_functional_group():
    msg = (
        "UNB+UNOC:3+S+R+260101:1200+REF1'"
        "UNG+ORDERS+S+R+260101:1200+G1+UN+D:24A'"
        "UNH+1+ORDERS:D:24A:UN'BGM+220'UNT+3+1'"
        "UNE+1+G1'"
        "UNZ+1+REF1'"
    )
    interchange = BaseParser().parse(msg)

    assert _one_line(interchange.dump_raw()) == msg


def test_functional_group_puts_multiple_messages_on_separate_lines():
    msg = (
        "UNB+UNOC:3+S+R+260101:1200+REF1'"
        "UNG+ORDERS+S+R+260101:1200+G1+UN+D:24A'"
        "UNH+1+ORDERS:D:24A:UN'BGM+220'UNT+3+1'"
        "UNH+2+ORDERS:D:24A:UN'BGM+220'UNT+3+2'"
        "UNE+2+G1'"
        "UNZ+1+REF1'"
    )
    interchange = BaseParser().parse(msg)

    assert "UNT+3+1'\nUNH+2+ORDERS:D:24A:UN'" in interchange.dump_raw()


def test_style_is_applied_only_to_target_component(valid_edifact_message):
    interchange = BaseParser().parse(valid_edifact_message)
    target = interchange.messages[0].trailer.data_elements[0].components[0]

    raw = interchange.dump_raw(target=target, style=_mark)

    assert "UNT+<11>+1'" in raw
    assert raw.count("<") == 1


def test_style_is_applied_to_target_segment(valid_edifact_message):
    interchange = BaseParser().parse(valid_edifact_message)
    target = interchange.messages[0].segments[0]

    raw = interchange.dump_raw(target=target, style=_mark)

    assert "<BGM+220+PO123456+9>'" in raw
    assert raw.count("<") == 1


def test_target_is_matched_by_identity_not_equality(valid_edifact_message):
    interchange = BaseParser().parse(valid_edifact_message)
    # Both NAD segments contain an equal "9" component; only the targeted instance must be styled.
    target = interchange.messages[0].segments[3].data_elements[1].components[2]

    raw = interchange.dump_raw(target=target, style=_mark)

    assert "NAD+BY+5412345000013::9'" in raw
    assert "NAD+SU+4012345000006::<9>'" in raw


def test_no_style_without_style_function(valid_edifact_message):
    interchange = BaseParser().parse(valid_edifact_message)
    target = interchange.messages[0].segments[0]

    assert interchange.dump_raw(target=target) == interchange.dump_raw()
