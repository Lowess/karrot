#!/usr/bin/env python
# -*- coding: utf-8 -*-

import structlog

# Import flask dependencies
from flask import Blueprint, request, jsonify, current_app as app

from datetime import datetime

logger = structlog.get_logger()

# Define a blueprint
config = Blueprint("config", __name__, url_prefix="/config")


@config.route("", methods=["GET"])
def display():
    logger.debug("Hit on /config endpoint")

    settings = {
        key: app.config[key] for key in app.config.keys() if key.startswith("KARROT_")
    }
    return jsonify(status="success", config=settings)
