#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.app import EventListener


if __name__ == "__main__":
    eventListener = EventListener()
    eventListener.start()
