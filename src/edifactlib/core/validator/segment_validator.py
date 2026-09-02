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
        """Validate a segment against its segment definition.

        Looks up the segment definition from the syntax or the directory and,
        for each expected data element position, checks whether required
        elements are present and the maximum repeat count is respected, then
        delegates the content validation of each occurrence found to the
        DataElementValidator.

        Args:
            segment: The segment to validate.
            version: The syntax version of the message.
            dir_name: Name of the message directory, if validation should be
                directory-specific, otherwise None for the generic syntax.
            header: The interchange header segment (UNB), passed through to
                the DataElementValidator for charset validation.
            una_seg: The UNA segment of the message, if present, otherwise
                None.

        Raises:
            SegmentValidationError: If the segment definition for the tag
                cannot be found, a required data element is missing, a data
                element occurs more often than allowed, or a required data
                element is present but its content is empty.
            DataElementValidationError: If a data element or component
                violates its definition.
        """
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
