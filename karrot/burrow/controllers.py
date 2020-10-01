#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 :synopsis: Burrow Blueprint

 Main application endpoint called by Burrow
"""

# Import flask dependencies
from structlog import get_logger
from flask import Blueprint, request, jsonify, current_app as app

# Define a blueprint
burrow = Blueprint("burrow", __name__, url_prefix="/burrow")
logger = get_logger()

################################################################################
# home blueprint functions
################################################################################


@burrow.route("", methods=["POST"])
def webhook_handler():
    """
    Process an incoming event from Burrow and call
    ``event_handler()`` to process it.

    :param str event: A valid Burrow Json event POSTed to this endpoint
    """
    logger.debug("Hit on /burrow endpoint")
    data = request.get_json()
    # TODO Deal with partial notifier failures with different return codes
    event_handler(data)
    return jsonify(data)


def event_handler(event):
    """
    For each enabled reporter, call the ``process(event)`` function.

    If ``prometheus`` is enabled, it tracks the reporter update.

    :param str event: A valid Burrow Json event
    """
    prom = app.config["REPORTERS"].get("prometheus", None)

    for _, reporter in app.config["REPORTERS"].items():
        reporter.process(event)
        if prom:
            prom.stats(reporter)
