# ---------------------------------------------------------------------------
# AI-generated: This code (or parts of it) was created with the assistance
# of AI (Claude) and has been reviewed/adapted.
# ---------------------------------------------------------------------------

import pytest

from edifactlib import Directory, Syntax

VALID_EDIFACT_MESSAGE = """UNA:+.? '
UNB+UNOC:3+5412345000013:14+4012345000006:14+260704:1200+REF00001'
UNH+1+ORDERS:D:24A:UN'
BGM+220+PO123456+9'
DTM+137:20260704:102'
NAD+BY+5412345000013::9'
NAD+SU+4012345000006::9'
LIN+1++4712345:EN'
QTY+21:100'
LIN+2++4798765:EN'
QTY+21:50'
UNS+S'
UNT+11+1'
UNZ+1+REF00001'
"""


@pytest.fixture
def valid_edifact_message() -> str:
    """The ORDERS example from the README, verified to parse/validate/resolve cleanly."""
    return VALID_EDIFACT_MESSAGE


@pytest.fixture
def syntax() -> Syntax:
    return Syntax()


@pytest.fixture
def directory() -> Directory:
    return Directory()
