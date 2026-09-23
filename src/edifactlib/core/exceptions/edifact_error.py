from ..models import ErrorDetails


class EdifactError(Exception):
    def __init__(self, message: str, details: ErrorDetails | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details if details is not None else ErrorDetails()

    def __str__(self) -> str:
        target = self.details.component or self.details.data_element or self.details.segment

        if not self.details.interchange or not target:
            return self.message

        interchange_text = self.details.interchange.dump_raw(None, target, self._red)
        return f"{self.message}\n\nFaulty part:\n{interchange_text}"

    def _red(self, text: str) -> str:
        return f"\033[31m{text}\033[0m"
