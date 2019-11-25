#!/usr/bin/env python
# -*- coding: utf-8 -*-

import structlog
from datetime import datetime
from munch import munchify

logger = structlog.get_logger()


class Reporter(object):
    def __init__(self, name):
        """
            Parent class defining common method and attributes for child Reporters.
        """
        self._name = name
        self._event = None
        self._last_event_ts = None

    def process(self, event):
        """
            Refresh the object with the event details.
            A child class should call this parent function
            and then implement the proper processing steps for the event.

            :param str event: A
        """
        self._event = munchify(event["Event"])
        self._last_event_ts = datetime.now()

    def stats(self, reporter):
        """
            Report stats of an other reporter. Useful for Prometheus to collect
            stats about other reporters.

            This method must be implemented in child classes.
        """
        pass
