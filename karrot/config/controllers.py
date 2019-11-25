#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 :synopsis: Configuration Blueprint

 Configuration endpoint for the application
"""

import structlog

# Import flask dependencies
from flask import Blueprint, jsonify, current_app as app

logger = structlog.get_logger()

# Define a blueprint
config = Blueprint("config", __name__, url_prefix="/config")


@config.route("", methods=["GET"])
def display():
    """
        Returns a simple JSON string with the current application configuration.

        :returns: json -- A JSON with the following format:
        ``{"status": "success", "settings": "{...}"}``
    """
    logger.debug("Hit on /config endpoint")

    settings = {
        key: app.config[key] for key in app.config.keys() if key.startswith("KARROT_")
    }
    return jsonify(status="success", config=settings)
