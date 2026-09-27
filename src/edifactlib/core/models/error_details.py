from pydantic import BaseModel

from .interchange import Component, DataElement, Interchange, Segment


class ErrorDetails(BaseModel):
    """Location of an error within a parsed interchange.

    Each field references the actual model instance from the parsed
    interchange, identifying the faulty part by identity rather than
    by copy. Validators fill in the fields bottom-up as the error
    propagates, so any field may still be None if the location is
    unknown or not applicable.
    """

    interchange: Interchange | None = None
    """The interchange in which the error occurred."""

    segment: Segment | None = None
    """The faulty segment, or the segment containing the faulty data element."""

    data_element: DataElement | None = None
    """The faulty data element, or the data element containing the faulty component."""

    component: Component | None = None
    """The faulty component."""
