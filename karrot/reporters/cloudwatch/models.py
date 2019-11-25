#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import datetime
import boto3
from botocore.exceptions import ClientError, ParamValidationError

from structlog import get_logger
from flask import current_app as app
from prometheus_client import Counter

from karrot.reporters.models import Reporter
from karrot.reporters.cloudwatch.utils import assumed_session


logger = get_logger(__name__)

CLOUDWATCH_API_CALLS_COUNT = Counter(
    "karrot_reporter_cloudwatch_api_count",
    "Number of calls made to Cloudwatch",
    labelnames=["reporter", "status"],
)


class CloudwatchReporter(Reporter):
    def __init__(self, name):
        super().__init__(name)

        iam_role = app.config["KARROT_IAM_ROLE"]

        try:
            if iam_role is not None:
                logger.info("Assuming IAM role", role=iam_role)
                self._client = assumed_session(
                    role_arn=iam_role, session_name="karrot"
                ).client("cloudwatch")
            else:
                self._client = boto3.client("cloudwatch")
                logger.info("Initialized boto client successfully")
        except (ClientError, ParamValidationError) as e:
            logger.exception("Cloudn't initialize boto client", error=str(e))
            sys.exit(1)

        self._metrics = []
        self._namespace = app.config["KARROT_CLOUDWATCH_NAMESPACE"]
        self._flush_interval = datetime.timedelta(
            seconds=int(app.config["KARROT_CLOUDWATCH_INTERVAL"])
        )
        self._last_flush_ts = datetime.datetime.now() - self._flush_interval

    def process(self, event):
        super().process(event)
        self._collect_lag_handler()
        self.stats(self)

    def stats(self, reporter):
        pass

    def _collect_lag_handler(self):
        metric_name = self._event.Result.group
        self._metrics.append(
            {
                "MetricName": metric_name,
                "Value": self._event.Result.totallag,
                "Timestamp": datetime.datetime.utcnow(),
            }
        )
        self._flush_lag_metrics()

    def _flush_lag_metrics(self, force=False):
        flush_max_size = 30000  # In bytes
        should_flush = False

        # Flush only when there are metrics
        if len(self._metrics) > 0:
            # Check the flush interval to determine if a flush should happen or not
            now = datetime.datetime.now()
            if now > (self._last_flush_ts + self._flush_interval):
                logger.debug(
                    "Flush triggered as flush interval has been reached",
                    now=now,
                    prev=self._last_flush_ts,
                )
                should_flush = True

            # Check if the payload is getting close to the request size limit (40Kb)
            if sys.getsizeof(self._metrics) >= flush_max_size:
                logger.debug(
                    "Flush triggered as payload size has been reached",
                    size=sys.getsizeof(self._metrics),
                    limit=30000,
                )
                should_flush = True

            # If metrics array has 20 elements a flush must be triggered
            if len(self._metrics) == 20:
                logger.debug(
                    "Flush triggered as MetricData cannot contain more than 20 metrics",
                    size=len(self._metrics),
                )
                should_flush = True

            # Forced flushed if needed
            if force:
                should_flush = True

        if should_flush:
            try:
                self._client.put_metric_data(
                    MetricData=self._metrics, Namespace=self._namespace
                )
                logger.info(
                    "Lag has been reported to Cloudwatch", count=len(self._metrics)
                )
                CLOUDWATCH_API_CALLS_COUNT.labels(
                    reporter=self._name, status="success"
                ).inc()

                self._last_flush_ts = datetime.datetime.now()
                self._metrics = []
            except Exception:
                logger.exception("Lag could not be reported to cloudwatch")
                CLOUDWATCH_API_CALLS_COUNT.labels(
                    reporter=self._name, status="error"
                ).inc()
