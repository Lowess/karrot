#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 :synopsis: Heartbeat Blueprint

 Heartbeat endpoint of the application
"""

# Import flask dependencies
from flask import Blueprint, jsonify, current_app as app

from datetime import datetime

# Define a blueprint
heartbeat = Blueprint("heartbeat", __name__, url_prefix="/heartbeat")


@heartbeat.route("", methods=["GET"])
def health():
    """
    Returns a simple JSON string when the application is healthy.

    :returns: json -- A JSON with the following format:
    ``{"status": "success",
       "msg": "Burrow-reporter is healthy",
       "time": "<datetime.now()>"}``
    """
    app.logger.debug("Healthcheck")
    return jsonify(status="success", msg="Karrot is healthy", time=str(datetime.now()))
