#!/usr/bin/env python
# -*- coding: utf-8 -*-

from karrot.reporters.prometheus.controllers import PrometheusReporter
from karrot.reporters.cloudwatch.controllers import CloudwatchReporter

class ReporterFactory(object):

    @staticmethod
    def get(reporter):
        """Return the proper notifier object based on the name"""
        if reporter == 'prometheus':
            return PrometheusReporter('prometheus')
        elif reporter == 'cloudwatch':
            return CloudwatchReporter('cloudwatch')
        else:
            raise ValueError(reporter)
