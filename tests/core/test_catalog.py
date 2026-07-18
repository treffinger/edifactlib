# ---------------------------------------------------------------------------
# AI-generated: This code (or parts of it) was created with the assistance
# of AI (Claude) and has been reviewed/adapted.
# ---------------------------------------------------------------------------

from unittest.mock import patch

import pytest

from edifactlib.core.exceptions import CatalogError


def test_syntax_get_segment_returns_known_definitions(syntax):
    for version in ("2", "3"):
        seg_def = syntax.get_segment("UNB", version)
        assert seg_def.tag == "UNB"
        assert seg_def.name == "Interchange header"


def test_syntax_get_composite(syntax):
    composite = syntax.get_composite("S009", "3")
    assert composite.name == "Message identifier"
    assert [c.tag for c in composite.components][:4] == ["0065", "0052", "0054", "0051"]


def test_syntax_get_element(syntax):
    element = syntax.get_element("0062", "3")
    assert element.name == "Message reference number"
    assert element.charset == "an"
    assert element.max_length == 14


def test_directory_get_segment_returns_known_definitions(directory):
    bgm = directory.get_segment("BGM", "D.24A")
    assert bgm.name == "Beginning of message"

    nad = directory.get_segment("NAD", "D.24A")
    assert nad.name == "Name and address"


def test_directory_get_composite(directory):
    composite = directory.get_composite("C507", "D.24A")
    assert composite.name == "Date/time/period"
    required_tags = [c.tag for c in composite.components if c.required]
    assert required_tags == ["2005"]


def test_directory_get_element(directory):
    element = directory.get_element("1004", "D.24A")
    assert element.name == "Document identifier"
    assert element.min_length == 1
    assert element.max_length == 70


def test_unknown_catalog_name_raises_catalog_error(directory):
    with pytest.raises(CatalogError):
        directory.get_segment("BGM", "NOPE.VERSION")


def test_catalog_is_loaded_lazily_and_only_once(syntax):
    assert syntax._loaded_catalogs == set()

    syntax.get_segment("UNB", "3")
    assert "3" in syntax._loaded_catalogs

    with patch.object(syntax, "_load", wraps=syntax._load) as load_spy:
        syntax.get_segment("UNH", "3")
        syntax.get_element("0062", "3")

        load_spy.assert_not_called()


def test_unknown_tag_in_loaded_catalog(directory):
    assert directory.get_segment("ZZZ", "D.24A") is None
