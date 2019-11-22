#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from karrot.reporters.prometheus.models import PrometheusReporter
from prometheus_client import REGISTRY
from flask import url_for

logger = logging.getLogger(__name__)


class TestPrometheusReporter:
    """TODO."""

    def test_models_process(self, events):
        reporter = PrometheusReporter("prometheus")

        for event in events:
            logger.info(f"Sending event to reporter: {event}")
            reporter.process(event=event)

            # Make sure Prometheus events counter was incremented
            assert (
                REGISTRY.get_sample_value(
                    "karrot_reporter_events_count_total",
                    labels={"reporter": reporter._name},
                )
                > 0.0
            )

            # Make sure Prometheus lag is matching totallag
            assert (
                REGISTRY.get_sample_value(
                    "karrot_consumer_lag",
                    labels={
                        "cluster": reporter._event.Result.cluster,
                        "consumer": reporter._event.Result.group,
                    },
                )
                == reporter._event.Result.totallag
            )

    def test_controllers_metrics(self, prometheus, client, tmpdir):
        # Check prometheus metrics endpoint
        logger.info("Calling prometheus /metrics endpoint")
        response = client.get(url_for("prometheus.metrics"))
        assert response.status_code == 200
