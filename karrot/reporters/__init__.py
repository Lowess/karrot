#!/usr/bin/env python
# -*- coding: utf-8 -*-

from munch import munchify
import structlog
from datetime import datetime

logger = structlog.get_logger()


class Reporter(object):

    def __init__(self, name, metrics_prefix):
        """
            Parent class defining common method and attributes for child Reporters.
        """
        self._name = name
        self._metrics_prefix = metrics_prefix
        self._event = None
        self._last_event_ts = None

    def process(self, event):
        self._event = munchify(event['Event'])
        self._last_event_ts = datetime.now()

    def stats(self, reporter):
        """
            Report stats of an other reporter. Useful for Prometheus to collect stats about
            other reporters.
        """
        pass
