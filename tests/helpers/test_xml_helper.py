#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from io import BytesIO

from lxml import etree

from app.helpers.events_parser import SubtitleEvent
from app.helpers.xml_helper import construct_request, NSMAP
from tests.resources.resources import construct_filename, load_resource

BASE_XPATH = "/tns:makeSubtitleAvailableRequest"


def test_construct_request_open():
    event = SubtitleEvent(load_resource("openOtAvailableEvent.xml"))
    xml = etree.parse(BytesIO(construct_request(event)))
    # Assert correct values in the XML
    assert _xml_value(xml, "/tns:requestor") == "VIAA"
    assert len(_xml_value(xml, "/tns:correlationId")) == 36
    assert _xml_value(xml, "/tns:id") == "media_id_open"
    assert _xml_value(xml, "/tns:otType") == "OPEN"
    assert _xml_value(xml, "/tns:destinationPath") == (
        "mam-collaterals/openOt/media_id_open"
    )

    # Assert validness according to schema
    assert _xml_valid_schema(xml)


def test_construct_request_closed():
    event = SubtitleEvent(load_resource("closedOtAvailableEvent.xml"))
    xml = etree.parse(BytesIO(construct_request(event)))
    # Assert correct values in the XML
    assert _xml_value(xml, "/tns:requestor") == "VIAA"
    assert len(_xml_value(xml, "/tns:correlationId")) == 36
    assert _xml_value(xml, "/tns:id") == "media_id_closed"
    assert _xml_value(xml, "/tns:otType") == "CLOSED"
    assert _xml_value(xml, "/tns:destinationPath") == (
        "mam-collaterals/closedOt/media_id_closed"
    )

    # Assert validness according to schema
    assert _xml_valid_schema(xml)


def _xml_value(xml, xpath: str) -> str:
    return xml.xpath(f"{BASE_XPATH}{xpath}", namespaces=NSMAP)[0].text


def _xml_valid_schema(xml) -> bool:
    # Load in XML schema
    schema = etree.XMLSchema(file=construct_filename("makeAvailableRequests.xsd"))
    # Assert validness according to schema
    return schema.validate(xml)
