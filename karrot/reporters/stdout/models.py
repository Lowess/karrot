#!/usr/bin/env python
# -*- coding: utf-8 -*-

from karrot.reporters.models import Reporter
from structlog import get_logger
import json

logger = get_logger()


class StdoutReporter(Reporter):
    def __init__(self, name):
        super().__init__(name)

    def process(self, event):
        super().process(event)
        logger.info(json.dumps(event))
        logger.info("Successfully processed burrow event", reporter=self._name)
