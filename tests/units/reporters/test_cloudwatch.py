#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import json

from prometheus_client import REGISTRY
from flask import url_for
from moto import mock_cloudwatch
from karrot.reporters.cloudwatch.models import CloudwatchReporter

logger = logging.getLogger(__name__)


class TestCloudwatchReporter:
    """TODO."""

    @mock_cloudwatch
    def test_process(self, app, events):
        reporter = CloudwatchReporter("cloudwatch")

        for _ in range(0, 21):
            for event in events:
                logger.info(f"Sending event to reporter: {event}")
                reporter.process(event=event)

        # logger.warning(
        #     REGISTRY.get_sample_value("karrot_reporter_cloudwatch_api_count")
        # )
