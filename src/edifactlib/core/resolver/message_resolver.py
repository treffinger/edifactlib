from ..directory import Directory
from ..exceptions import EdifactError
from ..models.interchange import Message
from ..syntax import Syntax
from .segment_resolver import SegmentResolver


class MessageResolver:
    def __init__(self, syntax: Syntax, directory: Directory) -> None:
        self._segment_resolver = SegmentResolver(syntax, directory)

    def resolve(self, message: Message, version: str) -> None:
        """Resolve the names of all segments of a message.

        Determines the message type/version from the UNH segment and passes
        it on to the SegmentResolver as the directory name. The UNS and TXT
        segments are resolved generically (without a directory), since they
        are not part of the message-specific definition.

        Args:
            message: The message whose segments should be resolved.
            version: The syntax version of the message.

        Raises:
            EdifactError: If the message identifier cannot be read from the
                message header.
        """
        try:
            msg_identifier = message.header.data_elements[1]
        except IndexError:
            raise EdifactError("The identifier of the message could not be read.")

        if len(msg_identifier.components) < 3:
            raise EdifactError("The identifier of the message could not be read.")

        dir_name = f"{msg_identifier.components[1].content}.{msg_identifier.components[2].content}"
        for segment in message.segments:
            if segment.tag == "UNS" or segment.tag == "TXT":
                self._segment_resolver.resolve(segment, version, None)
            else:
                self._segment_resolver.resolve(segment, version, dir_name)
