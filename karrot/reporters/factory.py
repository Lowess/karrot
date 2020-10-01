#!/usr/bin/env python
# -*- coding: utf-8 -*-

from karrot.reporters.prometheus.models import PrometheusReporter
from karrot.reporters.cloudwatch.models import CloudwatchReporter
from karrot.reporters.stdout.models import StdoutReporter


class ReporterFactory(object):
    """
    ReporterFactory used to create a Reporter object based on it's name.
    """

    @staticmethod
    def get(reporter):
        """
        Return the proper notifier object based on the name.

        :params str reporter: The type of reporter to create
        :returns: Reporter -- A reporter matching ``reporter``
        :raises: ValueError -- When the requested reporter is not found.
        """
        if reporter == "prometheus":
            return PrometheusReporter("prometheus")
        elif reporter == "cloudwatch":
            return CloudwatchReporter("cloudwatch")
        elif reporter == "stdout":
            return StdoutReporter("stdout")
        else:
            raise ValueError(reporter)
