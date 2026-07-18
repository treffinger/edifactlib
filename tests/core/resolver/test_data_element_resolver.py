# ---------------------------------------------------------------------------
# AI-generated: This code (or parts of it) was created with the assistance
# of AI (Claude) and has been reviewed/adapted.
# ---------------------------------------------------------------------------

import pytest

from edifactlib.core.directory import Directory
from edifactlib.core.models.interchange import Component, DataElement
from edifactlib.core.models.syntax import DataElementRef
from edifactlib.core.resolver.data_element_resolver import DataElementResolver
from edifactlib.core.syntax import Syntax


@pytest.fixture
def resolver() -> DataElementResolver:
    return DataElementResolver(Syntax(), Directory())


def test_eded_without_components_is_a_no_op(resolver):
    ref = DataElementRef(tag="1004", type="EDED", required=False, max_repeat=1)
    data_element = DataElement(components=[], position=1)

    resolver.resolve(data_element, ref, "3", "D.24A")

    assert data_element.name is None


def test_eded_resolves_name(resolver):
    ref = DataElementRef(tag="1004", type="EDED", required=True, max_repeat=1)
    data_element = DataElement(components=[Component(content="PO123456")], position=1)

    resolver.resolve(data_element, ref, "3", "D.24A")

    assert data_element.name == "Document identifier"


def test_eded_unknown_tag(resolver):
    ref = DataElementRef(tag="ZZZZ", type="EDED", required=False, max_repeat=1)
    data_element = DataElement(components=[Component(content="value")], position=1)

    assert resolver.resolve(data_element, ref, "3", "D.24A") is None


def test_edcd_resolves_composite_and_component_names(resolver):
    ref = DataElementRef(tag="C507", type="EDCD", required=True, max_repeat=1)
    data_element = DataElement(
        components=[Component(content="203"), Component(content="20260704"), Component(content="102")], position=0
    )

    resolver.resolve(data_element, ref, "3", "D.24A")

    assert data_element.name == "Date/time/period"
    assert data_element.components[0].name == "Date or time or period function code qualifier"
    assert data_element.components[1].name == "Date or time or period text"
    assert data_element.components[2].name == "Date or time or period format code"


def test_edcd_with_fewer_components_than_composite_def_stops_gracefully(resolver):
    ref = DataElementRef(tag="C507", type="EDCD", required=True, max_repeat=1)
    data_element = DataElement(components=[Component(content="203")], position=0)

    resolver.resolve(data_element, ref, "3", "D.24A")

    assert data_element.name == "Date/time/period"
    assert data_element.components[0].name == "Date or time or period function code qualifier"
