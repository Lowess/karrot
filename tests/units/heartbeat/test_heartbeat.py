#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from flask import url_for

logger = logging.getLogger(__name__)


class TestHeartbeat:
    """Test heartbeat Blueprint."""

    def test_controllers_heartbeat(self, prometheus, client):

        # Check prometheus metrics endpoint
        logger.info("Calling prometheus /heartbeat endpoint")
        response = client.get(url_for("heartbeat.health"))

        assert response.status_code == 200
        assert response.json["status"] == "success"
