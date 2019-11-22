#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

# Import flask dependencies
from structlog import get_logger
from flask import Blueprint, render_template, request, jsonify, current_app as app
from prometheus_client import (
    generate_latest,
    CollectorRegistry,
    CONTENT_TYPE_LATEST,
    Gauge,
    Counter,
)

# Define a blueprint
burrow = Blueprint("burrow", __name__, url_prefix="/burrow")
logger = get_logger()

################################################################################
# home blueprint functions
################################################################################


@burrow.route("", methods=["POST"])
def webhook_handler():
    logger.debug("Hit on /burrow endpoint")
    data = request.get_json()
    # TODO Deal with partial notifier failures with different return codes
    event_handler(data)
    return jsonify(data)


def event_handler(event):
    prom = app.config["REPORTERS"].get("prometheus", None)

    for _, reporter in app.config["REPORTERS"].items():
        reporter.process(event)
        if prom:
            prom.stats(reporter)
