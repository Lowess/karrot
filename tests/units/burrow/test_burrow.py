#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from prometheus_client import REGISTRY
from flask import url_for

logger = logging.getLogger(__name__)


class TestBurrrow:
    """Test heartbeat Blueprint."""

    def test_controllers_burrow(self, prometheus, client, events):
        logger.info("Testing Burrow")
        for event in events:
            logger.info(f"Sending event to /burrow endpoint: {event}")
            response = client.post(url_for("burrow.webhook_handler"), json=event)

            assert response.status_code == 200

            assert (
                REGISTRY.get_sample_value(
                    "karrot_reporter_events_count_total",
                    labels={"reporter": "cloudwatch"},
                )
                == 1.0
            )
