# ---------------------------------------------------------------------------
# AI-generated: This code (or parts of it) was created with the assistance
# of AI (Claude) and has been reviewed/adapted.
# ---------------------------------------------------------------------------

import pytest

from edifactlib.core.directory import Directory
from edifactlib.core.models.interchange import Component, DataElement, Segment
from edifactlib.core.resolver.segment_resolver import SegmentResolver
from edifactlib.core.syntax import Syntax


@pytest.fixture
def resolver() -> SegmentResolver:
    return SegmentResolver(Syntax(), Directory())


def test_resolves_segment_and_eded_data_element_name(resolver):
    nad = Segment(tag="NAD", data_elements=[DataElement(components=[Component(content="BY")], position=0)])

    resolver.resolve(nad, "3", "D.24A")

    assert nad.name == "Name and address"
    assert nad.data_elements[0].name == "Party function code qualifier"


def test_resolves_edcd_composite_and_component_names(resolver):
    dtm = Segment(
        tag="DTM",
        data_elements=[
            DataElement(
                components=[Component(content="203"), Component(content="20260704"), Component(content="102")],
                position=0,
            )
        ],
    )

    resolver.resolve(dtm, "3", "D.24A")

    assert dtm.name == "Date/time/period"
    assert dtm.data_elements[0].name == "Date/time/period"
    assert dtm.data_elements[0].components[0].name == "Date or time or period function code qualifier"
    assert dtm.data_elements[0].components[1].name == "Date or time or period text"
