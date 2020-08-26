#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  @Author: Rudolf De Geijter
#
#  app/services/rabbit.py
#

import time

from viaa.configuration import ConfigParser
from viaa.observability import logging

import pika


class RabbitClient:
    def __init__(self):
        configParser = ConfigParser()
        self.log = logging.get_logger(__name__, config=configParser)
        self.rabbitConfig = configParser.app_cfg["rabbitmq"]

        self.credentials = pika.PlainCredentials(
            self.rabbitConfig["username"], self.rabbitConfig["password"]
        )

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.rabbitConfig["host"],
                port=self.rabbitConfig["port"],
                credentials=self.credentials,
            )
        )

        self.channel = self.connection.channel()

    def send_message(self, body):
        try:
            self.channel.basic_publish(
                exchange=self.rabbitConfig["subtitle_outgoing_exchange"],
                routing_key=self.rabbitConfig["subtitle_outgoing_rk"],
                body=body,
            )

            return True

        except pika.exceptions.AMQPConnectionError as ce:
            raise ce

    def listen(self, on_message_callback, queue=None):
        if queue is None:
            queue = self.rabbitConfig["subtitle_incoming_queue"]

        try:
            while True:
                try:
                    channel = self.connection.channel()

                    channel.basic_consume(
                        queue=queue, on_message_callback=on_message_callback
                    )

                    channel.start_consuming()
                except pika.exceptions.StreamLostError:
                    self.logger.warning("RMQBridge lost connection, reconnecting...")
                    time.sleep(3)
                except pika.exceptions.ChannelWrongStateError:
                    self.logger.warning(
                        "RMQBridge wrong state in channel, reconnecting..."
                    )
                    time.sleep(3)
                except pika.exceptions.AMQPHeartbeatTimeout:
                    self.logger.warning(
                        "RMQBridge heartbeat timed out, reconnecting..."
                    )
                    time.sleep(3)

        except KeyboardInterrupt:
            self.channel.stop_consuming()

        self.connection.close()
