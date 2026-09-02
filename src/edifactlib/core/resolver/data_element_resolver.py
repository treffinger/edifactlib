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
        """Resolve the name of a data element (and its components, if any).

        Depending on the reference type (EDED = simple element, otherwise
        EDCD = composite element), looks up the element definition from the
        syntax or the directory and fills the resolved names into
        `data_element`. If no definition is found, the data element is left
        unchanged.

        Args:
            data_element: The data element to populate.
            data_element_ref: The reference definition from the segment
                definition.
            version: The syntax version of the message.
            dir_name: Name of the message directory if resolution should be
                directory-specific, otherwise None for the generic syntax.

        Raises:
            Does not raise any exception itself. Definitions that cannot be
            found are silently skipped; no name is set in that case.
        """
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
