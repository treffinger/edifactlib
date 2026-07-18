from ..directory import Directory
from ..models.interchange import Message
from ..syntax import Syntax
from .segment_resolver import SegmentResolver


class MessageResolver:
    def __init__(self, syntax: Syntax, directory: Directory) -> None:
        self._segment_resolver = SegmentResolver(syntax, directory)

    def resolve(self, message: Message, version: str) -> None:
        msg_identifier = message.header.data_elements[1]
        dir_name = f"{msg_identifier.components[1].content}.{msg_identifier.components[2].content}"
        for segment in message.segments:
            if segment.tag == "UNS" or segment.tag == "TXT":
                self._segment_resolver.resolve(segment, version, None)
            else:
                self._segment_resolver.resolve(segment, version, dir_name)
