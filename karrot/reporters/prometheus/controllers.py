#!/usr/bin/env python
# -*- coding: utf-8 -*-

from structlog import get_logger
from flask import Blueprint, Response, current_app as app
from prometheus_client import multiprocess
from prometheus_client import generate_latest, CollectorRegistry, CONTENT_TYPE_LATEST, Gauge, Counter

from karrot.reporters import Reporter

# Define a blueprint
prometheus = Blueprint('prometheus', __name__, url_prefix='/metrics')
logger = get_logger()

# http://<hostname>/metrics endpoint
@prometheus.route('', methods=['GET'])
def metrics():
    registry = CollectorRegistry()
    multiprocess.MultiProcessCollector(registry)
    data = generate_latest(registry)
    return Response(data, mimetype=CONTENT_TYPE_LATEST)


class PrometheusReporter(Reporter):

    def __init__(self, name, metrics_prefix):
        super().__init__(name, metrics_prefix)

        self._prom_total_lag = Gauge(f"{self._metrics_prefix}consumer_lag",
                                     "Total lag accumulated by the consumer",
                                     labelnames=['cluster', 'consumer'],
                                     multiprocess_mode='max')

        self._prom_reporters_events_count = Counter(f"{self._metrics_prefix}reporter_events_count",
                                                    "Number of events processed by the reporter",
                                                    labelnames=['reporter'])


    def process(self, event):
        super().process(event)
        self._kafka_lag_handler()
        self.stats(self)
        logger.info("Successfully processed burrow event", reporter=self._name)


    def stats(self, reporter):
        """
            Increment the number of events processed by the reporter.
        """
        self._prom_reporters_events_count.labels(reporter=reporter._name).inc()


    def _kafka_lag_handler(self):
        self._prom_total_lag.labels(cluster=self._event.Result.cluster,
                                  consumer=self._event.Result.group).set(self._event.Result.totallag)
