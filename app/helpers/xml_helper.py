#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from uuid import uuid4

from lxml import etree

from app.helpers.events_parser import SubtitleEvent

NAMESPACE_TNS = "http://www.vrt.be/mig/viaa"
NSMAP = {"tns": NAMESPACE_TNS}
REQUESTOR = "meemoo"


def construct_request(event: SubtitleEvent) -> str:
    """ Constructs the makeSubtitleAvailableRequest XML. """
    root = etree.Element(f"{{{NAMESPACE_TNS}}}makeSubtitleAvailableRequest", nsmap=NSMAP)
    etree.SubElement(root, f"{{{NAMESPACE_TNS}}}requestor").text = f"{REQUESTOR}"
    etree.SubElement(root, f"{{{NAMESPACE_TNS}}}correlationId").text = uuid4().hex
    etree.SubElement(root, f"{{{NAMESPACE_TNS}}}id").text = f"{event.media_id}"
    etree.SubElement(root, f"{{{NAMESPACE_TNS}}}destinationPath").text = (
        f"mam-collaterals/{event.destination_path_type()}/{event.media_id}"
    )
    etree.SubElement(root, f"{{{NAMESPACE_TNS}}}otType").text = f"{event.ot_type}"

    return etree.tostring(
        root, pretty_print=True, encoding="UTF-8", xml_declaration=True
    )
