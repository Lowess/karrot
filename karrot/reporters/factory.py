#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import current_app as app
from karrot.reporters.prometheus.controllers import PrometheusReporter
from karrot.reporters.cloudwatch.controllers import CloudwatchReporter


class ReporterFactory(object):

    @staticmethod
    def get(reporter):
        """Return the proper notifier object based on the name"""

        metrics_prefix = app.config["KARROT_PROMETHEUS_METRIC_PREFIX"]

        if reporter == 'prometheus':
            return PrometheusReporter('prometheus', metrics_prefix)
        elif reporter == 'cloudwatch':
            return CloudwatchReporter('cloudwatch', metrics_prefix)
        else:
            raise ValueError(reporter)
