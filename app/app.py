#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pika.exceptions import AMQPConnectionError
from viaa.configuration import ConfigParser
from viaa.observability import logging

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
        channel.basic_ack(delivery_tag=method.delivery_tag)

    def start(self):
        # Start listening for incoming messages
        self.log.info("Start to listen for messages...")
        self.rabbit_client.listen(self.handle_message)
