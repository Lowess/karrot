#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import json

from prometheus_client import REGISTRY
from flask import url_for
from moto import mock_cloudwatch
from karrot.reporters.cloudwatch.models import CloudwatchReporter

logger = logging.getLogger(__name__)


class TestConfig:
    """TODO."""

    def test_controllers_config(self, prometheus, client, tmpdir):

        # Check reporters endpoint
        logger.info("Calling Config endpoint")
        response = client.get(url_for("config.display"))
        assert response.status_code == 200
        for conf in response.json["config"]:
            assert conf.startswith("KARROT_")
