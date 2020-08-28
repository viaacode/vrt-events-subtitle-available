#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pika.exceptions import AMQPConnectionError, AMQPError
from viaa.configuration import ConfigParser
from viaa.observability import logging

from app.helpers.events_parser import SubtitleEvent, InvalidEventException
from app.helpers.xml_helper import construct_request
from app.services.rabbit import RabbitClient


class EventListener:
    def __init__(self):
        configParser = ConfigParser()
        self.log = logging.get_logger(__name__, config=configParser)
        self.config = configParser.app_cfg
        try:
            self.rabbit_client = RabbitClient()
        except AMQPConnectionError as error:
            self.log.error("Connection to RabbitMQ failed.")
            raise error

    def handle_message(self, channel, method, properties, body):
        """Main method that will handle the incoming messages."""
        # 1. Parse incoming message
        try:
            event = SubtitleEvent(body)
        except InvalidEventException as ex:
            self.log.warning("Invalid event received.", body=body, exception=ex)
            channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            return

        # 2. Transform message to makeSubtitleAvailableRequest
        request_message = construct_request(event)

        # 3. Send message to exchange
        try:
            self.rabbit_client.send_message(request_message)
        except AMQPError as error:
            self.log.critical(
                "Failed to publish message!",
                error=error,
                request_message=request_message,
            )
            channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            return

        # 4. Send ack back to RabbitMQ
        channel.basic_ack(delivery_tag=method.delivery_tag)

    def start(self):
        # Start listening for incoming messages
        self.log.info("Start to listen for messages...")
        self.rabbit_client.listen(self.handle_message)
