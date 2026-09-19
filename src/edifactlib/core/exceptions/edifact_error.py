from ..models import ErrorDetails
from ..models.interchange import ServiceCharacters


class EdifactError(Exception):
    code: str = "EDIFACT_ERROR"

    def __init__(self, message: str, details: ErrorDetails | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details if details is not None else ErrorDetails()

    def __str__(self) -> str:
        if not self.details.interchange:
            return self.message

        service_chars = (
            ServiceCharacters.from_una(self.details.interchange.una)
            if self.details.interchange.una
            else ServiceCharacters()
        )
        location = ""
        if self.details.component:
            location = self.details.component.dump_raw(service_chars)
        elif self.details.data_element:
            location = self.details.data_element.dump_raw(service_chars)
        elif self.details.segment:
            location = self.details.segment.dump_raw(service_chars)

        interchange_text = self.details.interchange.dump_raw()
        interchange_text = interchange_text.replace(location, f"\033[31m{location}\033[0m")
        return f"{self.message}\n\nFaulty part: \n\n{interchange_text}"
