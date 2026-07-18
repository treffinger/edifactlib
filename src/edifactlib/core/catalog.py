import json
from abc import ABC
from pathlib import Path

from .exceptions import CatalogError
from .models.syntax import CompositeDef, ElementDef, SegmentDef


class Catalog(ABC):
    def __init__(self, file: str, catalog_folder: str) -> None:
        self._base_path = Path(file).resolve().parent / catalog_folder
        self._segments: dict[str, dict[str, SegmentDef]] = {}
        self._composites: dict[str, dict[str, CompositeDef]] = {}
        self._elements: dict[str, dict[str, ElementDef]] = {}
        self._loaded_catalogs = set()

    def _load(self, catalog_name: str) -> None:
        file_path = self._base_path / f"{catalog_name}.json"

        try:
            with file_path.open() as f:
                raw_data = json.loads(f.read())
        except Exception as e:
            raise CatalogError(
                f'The Catalog "{catalog_name}" could not be found. The library may be outdated and therefore may not yet support this version.'
            ) from e

        self._segments[catalog_name] = {e.tag: e for e in (SegmentDef.model_validate(i) for i in raw_data["EDSD"])}
        self._composites[catalog_name] = {e.tag: e for e in (CompositeDef.model_validate(i) for i in raw_data["EDCD"])}
        self._elements[catalog_name] = {e.tag: e for e in (ElementDef.model_validate(i) for i in raw_data["EDED"])}
        self._loaded_catalogs.add(catalog_name)

    def _require_catalog(self, catalog_name) -> None:
        if catalog_name not in self._loaded_catalogs:
            self._load(catalog_name)

    def get_segment(self, tag: str, catalog_name: str) -> SegmentDef | None:
        self._require_catalog(catalog_name)
        return self._segments[catalog_name].get(tag)

    def get_composite(self, tag: str, catalog_name: str) -> CompositeDef | None:
        self._require_catalog(catalog_name)
        return self._composites[catalog_name].get(tag)

    def get_element(self, tag: str, catalog_name: str) -> ElementDef | None:
        self._require_catalog(catalog_name)
        return self._elements[catalog_name].get(tag)
