from ..exceptions import ParsingError
from ..models.interchange import Component, DataElement, FunctionalGroup, Interchange, Message, Segment


class BaseParser:
    def __init__(self) -> None:
        self._set_defaults()

    def parse(self, edifact_msg: str) -> Interchange:
        self._set_defaults()
        edifact_msg = self._remove_line_breaks(edifact_msg)

        if edifact_msg.startswith("UNA"):
            self._handle_custom_una(edifact_msg)

        segments = self._extract_segments(edifact_msg)
        interchange = self._create_interchange(segments)

        return interchange

    def _set_defaults(self) -> None:
        self._component_sep = ":"
        self._data_sep = "+"
        self._decimal_notation = "."
        self._release_indicator = "?"
        self._segment_terminator = "'"

    def _remove_line_breaks(self, edifact_msg: str) -> str:
        return edifact_msg.replace("\r", "").replace("\n", "")

    def _handle_custom_una(self, edifact_msg: str) -> None:
        self._component_sep = edifact_msg[3]
        self._data_sep = edifact_msg[4]
        self._decimal_notation = edifact_msg[5]
        self._release_indicator = edifact_msg[6]
        # Character 5 at index 7 is reserved for future use
        self._segment_terminator = edifact_msg[8]

    def _extract_segments(self, edifact_msg: str) -> list[Segment]:
        segments: list[Segment] = []
        una_skip = 0
        if edifact_msg.startswith("UNA"):
            una_skip = 9
            segments.append(
                Segment(
                    tag="UNA", data_elements=[DataElement(components=[Component(content=edifact_msg[3:9])], position=0)]
                )
            )

        segments_raw = self._split_respecting_release(edifact_msg[una_skip:], self._segment_terminator)[:-1]

        for segment_raw in segments_raw:
            data_elements_raw = self._split_respecting_release(segment_raw[4:], self._data_sep)
            data_elements: list[DataElement] = []
            for i, data_element_raw in enumerate(data_elements_raw):
                self._extract_data_element(data_element_raw, i, data_elements)

            tag = segment_raw[:3]
            segments.append(Segment(tag=tag, data_elements=data_elements))

        return segments

    def _extract_data_element(self, raw_data: str, position: int, data_elements: list[DataElement]) -> None:
        components: list[Component] = []
        for content in self._split_respecting_release(raw_data, self._component_sep):
            unescaped = self._unescape(content)
            if content != "":
                components.append(Component(content=unescaped))
        data_elements.append(DataElement(components=components, position=position))

    def _create_interchange(self, segments: list[Segment]) -> Interchange:
        if len(segments) < 4:
            raise ParsingError("Interchange could not be parsed.")

        i = 1
        una: Segment | None = None
        header = segments[0]
        if segments[0].tag == "UNA":
            una = segments[0]
            header = segments[1]
            i = 2

        messages: list[Message] = []
        functional_groups: list[FunctionalGroup] = []

        while i < len(segments) and segments[i].tag != "UNZ":
            match segments[i].tag:
                case "UNH":
                    m, i = self._parse_message(segments, i)
                    messages.append(m)
                case "UNG":
                    fg, i = self._parse_functional_group(segments, i)
                    functional_groups.append(fg)
                case _:
                    raise ParsingError(
                        f"The Interchange could not be parsed. A UNH or UNG segment is required, but neither was provided. Segment provided: {segments[i].tag}"
                    )

        if i >= len(segments):
            raise ParsingError("The Interchange could not be parsed. The interchange does not contain an UNZ segment.")

        return Interchange(
            una=una,
            header=header,
            trailer=segments[i],
            messages=messages,
            functional_groups=functional_groups,
        )

    def _parse_message(self, segments: list[Segment], i: int) -> tuple[Message, int]:
        msg_seg: list[Segment] = []
        header = segments[i]
        i += 1

        while segments[i].tag != "UNT":
            msg_seg.append(segments[i])
            i += 1
            if i >= len(segments):
                raise ParsingError("Interchange could not be parsed. The UNH segment was never closed.")

        trailer = segments[i]
        return Message(header=header, trailer=trailer, segments=msg_seg), i + 1

    def _parse_functional_group(self, segments: list[Segment], i: int) -> tuple[FunctionalGroup, int]:
        messages: list[Message] = []
        header = segments[i]
        i += 1

        while segments[i].tag != "UNE":
            m, i = self._parse_message(segments, i)
            messages.append(m)

        trailer = segments[i]
        i += 1
        return FunctionalGroup(header=header, trailer=trailer, messages=messages), i

    def _split_respecting_release(self, text: str, delimiter: str) -> list[str]:
        tokens: list[str] = []
        current: list[str] = []
        escaped = False

        for c in text:
            if escaped:
                current.append(c)
                escaped = False
            elif c == self._release_indicator:
                current.append(c)
                escaped = True
            elif c == delimiter:
                tokens.append("".join(current))
                current.clear()
            else:
                current.append(c)

        tokens.append("".join(current))
        return tokens

    def _unescape(self, text: str) -> str:
        result: list[str] = []
        escaped = False

        for c in text:
            if escaped:
                result.append(c)
                escaped = False
            elif c == self._release_indicator:
                escaped = True
            else:
                result.append(c)

        return "".join(result)
