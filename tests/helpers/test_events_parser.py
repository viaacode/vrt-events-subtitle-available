#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from app.helpers.events_parser import SubtitleEvent, InvalidEventException
from tests.resources.resources import load_resource


def test_closed_ot_available():
    event = SubtitleEvent(load_resource("closedOtAvailableEvent.xml"))
    assert event.media_id == "media_id_closed"
    assert event.ot_type == "CLOSED"
    assert event.destination_path_type() == "closedOt"


def test_open_ot_available():
    event = SubtitleEvent(load_resource("openOtAvailableEvent.xml"))
    assert event.media_id == "media_id_open"
    assert event.ot_type == "OPEN"
    assert event.destination_path_type() == "openOt"


def test_unknown_event():
    with pytest.raises(InvalidEventException) as error:
        SubtitleEvent(load_resource("unknownOtAvailableEvent.xml"))
    assert "unknownOtAvailableEvent" in error.value.message
