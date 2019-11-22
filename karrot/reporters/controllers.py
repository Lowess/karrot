#!/usr/bin/env python
# -*- coding: utf-8 -*-

import structlog
from flask import Blueprint, jsonify, current_app as app

logger = structlog.get_logger()

# Define a blueprint
reporters = Blueprint("reporters", __name__, url_prefix="/reporters")

# http://<hostname>/metrics endpoint
@reporters.route("/", defaults={"reporter": None}, methods=["GET"])
@reporters.route("/<reporter>", methods=["GET"])
def display(reporter):
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
