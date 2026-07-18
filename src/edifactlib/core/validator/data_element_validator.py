from ..directory import Directory
from ..exceptions import DataElementValidationError
from ..models.interchange import DataElement, Segment
from ..models.syntax import CompositeDef, DataElementRef, ElementDef
from ..syntax import Syntax
from .component_validator import ComponentValidator


class DataElementValidator:
    def __init__(self, syntax: Syntax, directory: Directory) -> None:
        self._component_validator = ComponentValidator()
        self._syntax = syntax
        self._directory = directory

    def validate(
        self,
        data_element: DataElement,
        data_element_ref: DataElementRef,
        version: str,
        dir_name: str | None,
        header: Segment,
        una_seg: Segment | None,
    ) -> None:
        if not data_element_ref.required and not data_element.components:
            return

        if data_element_ref.type == "EDED":
            self._validate_eded(data_element, data_element_ref, version, dir_name, header, una_seg)
        else:
            self._validate_edcd(data_element, data_element_ref, version, dir_name, header, una_seg)

    def _validate_eded(
        self,
        data_element: DataElement,
        data_element_ref: DataElementRef,
        version: str,
        dir_name: str | None,
        header: Segment,
        una_seg: Segment | None,
    ) -> None:
        if len(data_element.components) > 1:
            raise DataElementValidationError(
                f"The data element {data_element_ref.tag} is not a composite element, but it contains multiple values."
            )

        if not data_element.components[0].content and data_element_ref.required:
            raise DataElementValidationError(f"The data element {data_element_ref.tag} is required but is missing.")

        element_def: ElementDef | None = None
        if not dir_name:
            element_def = self._syntax.get_element(data_element_ref.tag, version)
        else:
            element_def = self._directory.get_element(data_element_ref.tag, dir_name)

        if not element_def:
            raise DataElementValidationError(f"The data element {data_element_ref.tag} could not be found.")

        self._component_validator.validate(data_element.components[0], element_def, header, una_seg)

    def _validate_edcd(
        self,
        data_element: DataElement,
        data_element_ref: DataElementRef,
        version: str,
        dir_name: str | None,
        header: Segment,
        una_seg: Segment | None,
    ) -> None:
        composite_def: CompositeDef | None = None
        if not dir_name:
            composite_def = self._syntax.get_composite(data_element_ref.tag, version)
        else:
            composite_def = self._directory.get_composite(data_element_ref.tag, dir_name)

        if not composite_def:
            raise DataElementValidationError(f"The composite data element {data_element_ref.tag} could not be found.")

        for i, component_ref in enumerate(composite_def.components):
            if i >= len(data_element.components):
                if component_ref.required:
                    raise DataElementValidationError(
                        f'A component in the data element "{data_element_ref.tag}" is missing.'
                    )
                continue

            element_def: ElementDef | None = None
            if not dir_name:
                element_def = self._syntax.get_element(component_ref.tag, version)
            else:
                element_def = self._directory.get_element(component_ref.tag, dir_name)

            if not element_def:
                raise DataElementValidationError(f"The data element {component_ref.tag} could not be found.")

            self._component_validator.validate(data_element.components[i], element_def, header, una_seg)
