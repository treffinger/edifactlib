from ..directory import Directory
from ..exceptions import EdifactError
from ..models.interchange import Interchange, Segment
from ..syntax import Syntax
from .message_resolver import MessageResolver
from .segment_resolver import SegmentResolver


class InterchangeResolver:
    def __init__(self) -> None:
        syntax = Syntax()
        directory = Directory()
        self._message_resolver = MessageResolver(syntax, directory)
        self._segment_resolver = SegmentResolver(syntax, directory)

    def resolve(self, interchange: Interchange) -> None:
        """Resolve the names of all segments/data elements of an interchange.

        First determines the syntax version from the interchange header, then
        resolves the header, the trailer, and all messages (either directly
        in the interchange or inside functional groups).

        Args:
            interchange: The interchange whose segments/data elements should
                be enriched with human-readable names.

        Raises:
            EdifactError: If the syntax version cannot be read from the
                interchange header.
        """
        version = self._get_version(interchange.header)
        self._segment_resolver.resolve(interchange.header, version, None)
        self._segment_resolver.resolve(interchange.trailer, version, None)

        for msg in interchange.messages:
            self._message_resolver.resolve(msg, version)

        for fg in interchange.functional_groups:
            for msg in fg.messages:
                self._message_resolver.resolve(msg, version)

    def _get_version(self, header: Segment) -> str:
        try:
            version = header.data_elements[0].components[1].content
        except IndexError:
            raise EdifactError("The syntax version of the interchange could not be read.")

        if not version:
            raise EdifactError("The syntax version of the interchange could not be read.")

        return version
