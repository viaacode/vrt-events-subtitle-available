#!/usr/bin/env python
# -*- coding: utf-8 -*-

from viaa.configuration import ConfigParser
from viaa.observability import logging


class EventListener:
    def __init__(self):
        configParser = ConfigParser()
        self.log = logging.get_logger(__name__, config=configParser)
        self.config = configParser.app_cfg

    def start(self):
        # Start listening for incoming messages
        self.log.info("Start to listen for messages...")
