from ..models import ErrorLocation


class EdifactError(Exception):
    code: str = "EDIFACT_ERROR"

    def __init__(self, message: str, location: ErrorLocation | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.location = location if location is not None else ErrorLocation()

    def __str__(self) -> str:
        sub_text = ""
        if self.location.component:
            sub_text = self.location.component.dump_raw()
        elif self.location.data_element:
            sub_text = self.location.data_element.dump_raw()
        elif self.location.segment:
            sub_text = self.location.segment.dump_raw()

        message_text = ""
        if self.location.message:
            message_text = self.location.message.dump_raw()
            message_text = message_text.replace(sub_text, f"\033[31m{sub_text}\033[0m")

        return f"{self.message}\n\nFaulty part: {sub_text}\n\nMessage:\n\n{message_text}"
