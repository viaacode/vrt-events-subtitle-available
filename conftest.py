#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest


@pytest.fixture(autouse=True)
def env_setup(monkeypatch):
    monkeypatch.setenv("RABBITMQ_USERNAME", "username")
    monkeypatch.setenv("RABBITMQ_PASSWORD", "password")
    monkeypatch.setenv("RABBITMQ_HOST", "host")
    monkeypatch.setenv("RABBITMQ_QUEUE", "queue")
    monkeypatch.setenv("RABBITMQ_SUBTITLE_INCOMING_QUEUE", "queue")
    monkeypatch.setenv("RABBITMQ_SUBTITLE_OUTGOING_EXCHANGE", "exchange")
    monkeypatch.setenv("RABBITMQ_SUBTITLE_OUTGOING_RK", "rk")
