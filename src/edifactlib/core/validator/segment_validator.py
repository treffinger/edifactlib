from ..directory import Directory
from ..exceptions import SegmentValidationError
from ..models.interchange import DataElement, Segment
from ..models.syntax import SegmentDef
from ..syntax import Syntax
from .data_element_validator import DataElementValidator


class SegmentValidator:
    def __init__(self, syntax: Syntax, directory: Directory) -> None:
        self._data_element_validator = DataElementValidator(syntax, directory)
        self._syntax = syntax
        self._directory = directory

    def validate(
        self, segment: Segment, version: str, dir_name: str | None, header: Segment, una_seg: Segment | None
    ) -> None:
        seg_def = self._get_segment_def(segment.tag, dir_name, version)
        by_position: dict[int, list[DataElement]] = {}

        for e in segment.data_elements:
            by_position.setdefault(e.position, []).append(e)

        for i, data_element_ref in enumerate(seg_def.data_elements):
            occurrences = by_position.get(i)

            if data_element_ref.required and not occurrences:
                raise SegmentValidationError(
                    f'The data element "{data_element_ref.tag}" is a required element, but was not specified.'
                )

            if not occurrences:
                continue

            if len(occurrences) > data_element_ref.max_repeat:
                raise SegmentValidationError(
                    f'The data element "{data_element_ref.tag}" occurs too many times. Allowed repetitions: {data_element_ref.max_repeat}, actual repetitions: {len(occurrences)}'
                )

            for occurrence in occurrences:
                if data_element_ref.required and not occurrence.components:
                    raise SegmentValidationError(
                        f"The data element {data_element_ref.tag} is required, but its entire content is empty"
                    )
                self._data_element_validator.validate(occurrence, data_element_ref, version, dir_name, header, una_seg)

    def _get_segment_def(self, tag: str, dir_name: str | None, version: str) -> SegmentDef:
        seg_def: SegmentDef | None = None
        if not dir_name:
            seg_def = self._syntax.get_segment(tag, version)
        else:
            seg_def = self._directory.get_segment(tag, dir_name)

        if not seg_def:
            raise SegmentValidationError(f'The tag "{tag}" was not found in the directory.')

        return seg_def
