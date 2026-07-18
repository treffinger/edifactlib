from ..directory import Directory
from ..models.interchange import DataElement
from ..models.syntax import CompositeDef, DataElementRef, ElementDef
from ..syntax import Syntax


class DataElementResolver:
    def __init__(self, syntax: Syntax, directory: Directory) -> None:
        self._syntax = syntax
        self._directory = directory

    def resolve(
        self, data_element: DataElement, data_element_ref: DataElementRef, version: str, dir_name: str | None
    ) -> None:
        if data_element_ref.type == "EDED":
            self._resolve_eded(data_element, data_element_ref, version, dir_name)
        else:
            self._resolve_edcd(data_element, data_element_ref, version, dir_name)

    def _resolve_eded(
        self, data_element: DataElement, data_element_ref: DataElementRef, version: str, dir_name: str | None
    ) -> None:
        if not data_element.components:
            return

        element_def: ElementDef | None = None
        if not dir_name:
            element_def = self._syntax.get_element(data_element_ref.tag, version)
        else:
            element_def = self._directory.get_element(data_element_ref.tag, dir_name)

        if not element_def:
            return

        data_element.name = element_def.name

    def _resolve_edcd(
        self, data_element: DataElement, data_element_ref: DataElementRef, version: str, dir_name: str | None
    ) -> None:
        composite_def: CompositeDef | None = None
        if not dir_name:
            composite_def = self._syntax.get_composite(data_element_ref.tag, version)
        else:
            composite_def = self._directory.get_composite(data_element_ref.tag, dir_name)

        if not composite_def:
            return

        data_element.name = composite_def.name

        for i, component_ref in enumerate(composite_def.components):
            if i >= len(data_element.components):
                break

            element_def: ElementDef | None = None
            if not dir_name:
                element_def = self._syntax.get_element(component_ref.tag, version)
            else:
                element_def = self._directory.get_element(component_ref.tag, dir_name)

            if not element_def:
                return

            data_element.components[i].name = element_def.name
