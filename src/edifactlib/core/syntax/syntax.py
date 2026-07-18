from ..catalog import Catalog


class Syntax(Catalog):
    def __init__(self) -> None:
        super().__init__(__file__, "versions")
