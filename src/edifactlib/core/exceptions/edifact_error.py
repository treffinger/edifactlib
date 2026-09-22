from ..models import ErrorDetails


class EdifactError(Exception):
    code: str = "EDIFACT_ERROR"

    def __init__(self, message: str, details: ErrorDetails | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details if details is not None else ErrorDetails()

    def __str__(self) -> str:
        if not self.details.interchange:
            return self.message

        target = self.details.component or self.details.data_element or self.details.segment
        interchange_text = self.details.interchange.dump_raw(None, target, self._red)
        return f"{self.message}\n\nFaulty part: \n\n{interchange_text}"

    def _red(self, text: str) -> str:
        return f"\033[31m{text}\033[0m"
