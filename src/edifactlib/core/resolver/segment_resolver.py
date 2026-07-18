from ..directory import Directory
from ..models.interchange import DataElement, Segment
from ..models.syntax import SegmentDef
from ..syntax import Syntax
from .data_element_resolver import DataElementResolver


class SegmentResolver:
    def __init__(self, syntax: Syntax, directory: Directory) -> None:
        self._data_element_resolver = DataElementResolver(syntax, directory)
        self._syntax = syntax
        self._directory = directory

    def resolve(self, segment: Segment, version: str, dir_name: str | None) -> None:
        seg_def: SegmentDef | None = None
        if not dir_name:
            seg_def = self._syntax.get_segment(segment.tag, version)
        else:
            seg_def = self._directory.get_segment(segment.tag, dir_name)

        if not seg_def:
            return

        segment.name = seg_def.name

        by_position: dict[int, list[DataElement]] = {}
        for e in segment.data_elements:
            by_position.setdefault(e.position, []).append(e)

        for i, data_element_ref in enumerate(seg_def.data_elements):
            occurrences = by_position.get(i)

            if not occurrences:
                continue

            for occurrence in occurrences:
                self._data_element_resolver.resolve(occurrence, data_element_ref, version, dir_name)
