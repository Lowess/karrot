#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 :synopsis: Reporter Blueprint

 Reporter endpoint of the application
"""

import structlog
from flask import Blueprint, jsonify, current_app as app

logger = structlog.get_logger()

# Define a blueprint
reporters = Blueprint("reporters", __name__, url_prefix="/reporters")

# http://<hostname>/metrics endpoint
@reporters.route("/", defaults={"reporter": None}, methods=["GET"])
@reporters.route("/<reporter>", methods=["GET"])
def display(reporter):
    """
        Returns a simple JSON with the current application reporters.

        :param str reporter: If provided returns details about this reporter only
        :returns: json -- A JSON with the following format:
        ``{"reporters": ["reporter1", "reporter2"]}``
    """
    logger.debug(f"{reporter}")
    data = {"reporters": []}

    for key, val in app.config["REPORTERS"].items():
        if reporter == key:
            data["reporters"].append(
                {
                    f"{key}": {
                        "last_event_timestamp": val._last_event_ts,
                        "last_event": val._event,
                    }
                }
            )
        if reporter is None:
            data["reporters"].append(key)

    return jsonify(data)
