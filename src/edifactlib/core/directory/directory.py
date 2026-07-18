from ..catalog import Catalog


class Directory(Catalog):
    def __init__(self) -> None:
        super().__init__(__file__, "directories")
