#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unittest.mock import MagicMock, patch

from pika.exceptions import AMQPError

from app.app import EventListener
from app.helpers.events_parser import InvalidEventException


@patch('app.app.RabbitClient')
@patch('app.app.SubtitleEvent')
@patch('app.app.construct_request')
def test_handle_message(mock_construct_request, mock_subtitle_event, mock_rabbit_client):
    event_listener = EventListener()
    incoming_message = "message"
    mock_channel = MagicMock()
    mock_method = MagicMock()
    # channel, method, properties, body
    event_listener.handle_message(mock_channel, mock_method, MagicMock(), incoming_message)

    assert mock_subtitle_event.call_count == 1
    assert mock_subtitle_event.call_args[0][0] == incoming_message
    event = mock_subtitle_event()

    assert mock_construct_request.call_count == 1
    assert mock_construct_request.call_args[0][0] == event
    request_message = mock_construct_request()

    assert mock_rabbit_client().send_message.call_count == 1
    assert mock_rabbit_client().send_message.call_args[0][0] == request_message

    assert mock_channel.basic_ack.call_count == 1
    assert mock_channel.basic_ack.call_args[1]["delivery_tag"] == mock_method.delivery_tag


@patch('app.app.RabbitClient')
@patch('app.app.SubtitleEvent')
@patch('app.app.construct_request')
def test_handle_message_invalid_event(mock_construct_request, mock_subtitle_event, mock_rabbit_client):
    event_listener = EventListener()
    incoming_message = "message"
    mock_channel = MagicMock()
    mock_method = MagicMock()
    mock_subtitle_event.side_effect = InvalidEventException("error")

    # channel, method, properties, body
    event_listener.handle_message(mock_channel, mock_method, MagicMock(), incoming_message)

    assert mock_subtitle_event.call_count == 1

    assert mock_construct_request.call_count == 0
    assert mock_rabbit_client().send_message.call_count == 0

    assert mock_channel.basic_ack.call_count == 0
    assert mock_channel.basic_nack.call_count == 1
    assert not mock_channel.basic_nack.call_args[1]["requeue"]


@patch('app.app.RabbitClient')
@patch('app.app.SubtitleEvent')
@patch('app.app.construct_request')
def test_handle_message_send_error(mock_construct_request, mock_subtitle_event, mock_rabbit_client):
    event_listener = EventListener()
    incoming_message = "message"
    mock_channel = MagicMock()
    mock_method = MagicMock()
    mock_rabbit_client().send_message.side_effect = AMQPError()

    # channel, method, properties, body
    event_listener.handle_message(mock_channel, mock_method, MagicMock(), incoming_message)

    assert mock_subtitle_event.call_count == 1

    assert mock_construct_request.call_count == 1
    assert mock_rabbit_client().send_message.call_count == 1

    assert mock_channel.basic_ack.call_count == 0
    assert mock_channel.basic_nack.call_count == 1
    assert not mock_channel.basic_nack.call_args[1]["requeue"]


@patch('app.app.RabbitClient')
def test_start(mock_rabbit_client):
    event_listener = EventListener()
    event_listener.start()

    assert mock_rabbit_client().listen.call_count == 1
    assert mock_rabbit_client().listen.call_args[0][0] == event_listener.handle_message
