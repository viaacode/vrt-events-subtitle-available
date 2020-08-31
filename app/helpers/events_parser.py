#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from io import BytesIO
from lxml import etree

# Constants
NAMESPACES = {
    "vrt": "http://www.vrt.be/mig/viaa/api",
    "dc": "http://purl.org/dc/elements/1.1/",
    "ebu": "urn:ebu:metadata-schema:ebuCore_2012",
}
ROOT_TAG_TYPES = {
    "openOtAvailableEvent": "OPEN",
    "closedOtAvailableEvent": "CLOSED"
}


class InvalidEventException(Exception):
    def __init__(self, message, **kwargs):
        self.message = message
        self.kwargs = kwargs


class SubtitleEvent():
    """ Convenience class for an XML subtitle available event. """
    def __init__(self, xml: bytes):
        self.event = self._get_subtitle_event(xml)
        self.ot_type = self._get_ot_type()
        self.media_id = self._get_xpath_from_event(
            "//ebu:identifier[@typeDefinition='MEDIA_ID']/dc:identifier"
        )

    def _get_subtitle_event(self, xml: bytes):
        """ Parses the input XML to a DOM.

        Raises:
            InvalidEventException -- When the XML is not valid.
        """
        try:
            tree = etree.parse(BytesIO(xml))
        except etree.XMLSyntaxError:
            raise InvalidEventException("Event is not valid XML.")
        return tree

    def _get_ot_type(self) -> str:
        """ Parses the root tag and determines the type based on it.

        Raises:
            InvalidEventException -- If root tag is unknown.

        Returns:
            str -- 'OPEN' if openOtAvailableEvent, 'CLOSED' if closedOtAvailableEvent.
        """
        root_tag = etree.QName(self.event.getroot()).localname
        try:
            return ROOT_TAG_TYPES[root_tag]
        except KeyError:
            raise InvalidEventException(
                f"Unknown event for root tag: '{root_tag}'."
            )

    def _get_xpath_from_event(self, xpath) -> str:
        """ Parses value based on an xpath.

        Raises:
            InvalidEventException -- When XPATH is mandatory but not present.
        """
        try:
            return self.event.xpath(xpath, namespaces=NAMESPACES)[0].text
        except IndexError:
            raise InvalidEventException(f"'{xpath}' is not present in the event.")

    def destination_path_type(self) -> str:
        """ calculates a subpath of the destination based on the caption type.

        Returns:
            str -- 'closedOt' if closedOtAvailableEvent
                   'openOt' if openOtAvailableEvent
        """
        return f"{self.ot_type.lower()}Ot"
