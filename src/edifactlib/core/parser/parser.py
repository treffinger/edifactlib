import re

from ..exceptions import ParsingError
from ..models.interchange import Interchange
from ..validator import InterchangeValidator
from .base_parser import BaseParser


class Parser:
    def __init__(self) -> None:
        self._validator = InterchangeValidator()
        self._parsers = {
            2: BaseParser(),
            3: BaseParser(),
        }

    def parse(self, edifact_msg: str, validate: bool = True) -> Interchange:
        version = self._get_version(edifact_msg)
        parser = self._parsers.get(version)

        if not parser:
            raise ParsingError("Interchange cannot be parsed. Invalid version number provided.")

        interchange = parser.parse(edifact_msg)
        if validate:
            self._validator.validate(interchange)

        return interchange

    def _get_version(self, edifact_msg: str) -> int:
        component_sep, data_sep = self._get_separator(edifact_msg)

        result = re.search(rf"UNB{re.escape(data_sep)}.{{4}}{re.escape(component_sep)}(\d)", edifact_msg)
        if not result:
            raise ParsingError("Interchange cannot be parsed.")

        try:
            return int(result.group(1))
        except Exception:
            raise ParsingError("Interchange cannot be parsed. Invalid version number provided.")

    def _get_separator(self, edifact_msg: str) -> tuple[str, str]:
        if not edifact_msg.startswith("UNA"):
            return ":", "+"

        if len(edifact_msg) > 4:
            return edifact_msg[3], edifact_msg[4]
        else:
            raise ParsingError("Interchange cannot be parsed. Invalid UNA segment provided.")
