#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from flask import url_for

logger = logging.getLogger(__name__)


class TestReporter:
    """TODO."""

    def test_controllers_reporters(self, prometheus, client, tmpdir):

        reporters = [
            "cloudwatch",
            "prometheus",
        ]

        # Check reporters endpoint
        logger.info("Calling prometheus /reporters endpoint")
        response = client.get(url_for("reporters.display"))
        assert response.status_code == 200
        assert sorted(response.json["reporters"]) == sorted(reporters)

        for reporter in reporters:
            response = client.get(url_for("reporters.display", reporter=reporter))
            assert response.status_code == 200
