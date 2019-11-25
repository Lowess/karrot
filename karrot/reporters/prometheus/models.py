#!/usr/bin/env python
# -*- coding: utf-8 -*-

from karrot.reporters.models import Reporter
from structlog import get_logger
from prometheus_client import Counter, Gauge

logger = get_logger()

PROM_TOTAL_LAG = Gauge(
    "karrot_consumer_lag",
    "Total lag accumulated by the consumer",
    labelnames=["cluster", "consumer"],
    multiprocess_mode="max",
)

REPORTER_EVENTS_COUNT = Counter(
    "karrot_reporter_events_count",
    "Number of events processed by the reporter",
    labelnames=["reporter"],
)


class PrometheusReporter(Reporter):
    def __init__(self, name):
        super().__init__(name)

    def process(self, event):
        super().process(event)
        self._kafka_lag_handler()
        self.stats(self)
        logger.info("Successfully processed burrow event", reporter=self._name)

    def stats(self, reporter):
        """
            Increment the number of events processed by the reporter.
        """
        REPORTER_EVENTS_COUNT.labels(reporter=reporter._name).inc()

    def _kafka_lag_handler(self):
        PROM_TOTAL_LAG.labels(
            cluster=self._event.Result.cluster, consumer=self._event.Result.group
        ).set(self._event.Result.totallag)
