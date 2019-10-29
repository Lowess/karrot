#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import flask dependencies
from flask import Blueprint, request, jsonify, current_app as app

from datetime import datetime

# Define a blueprint
heartbeat = Blueprint('heartbeat', __name__, url_prefix='/heartbeat')

# http://<hostname>/heartbeat endpoint
@heartbeat.route('', methods=['GET'])
def health():
    app.logger.debug("Healthcheck")
    return jsonify(status="success",
                   msg="Burrow-reporter is healthy",
                   time=str(datetime.now()))
