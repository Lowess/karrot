#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

# Import flask dependencies
from structlog import get_logger
from flask import Blueprint, render_template, request, jsonify, current_app as app
from prometheus_client import generate_latest, CollectorRegistry, CONTENT_TYPE_LATEST, Gauge, Counter

from karrot import REPORTERS

# Define a blueprint
burrow = Blueprint('burrow', __name__, url_prefix='/')
logger = get_logger()

################################################################################
# home blueprint functions
################################################################################

@burrow.route('burrow', methods=['POST'])
def webhook_handler():
    logger.info('Hit on /burrow endpoint')
    data = request.get_json()
    # logger.info(f'{json.dumps(data, indent=4)}')
    event_handler(data)
    # TODO Deal with partial notifier failures with different return codes
    return jsonify(data)


def event_handler(event):
    prom = REPORTERS.get('prometheus', None)

    for _, reporter in REPORTERS.items():
        reporter.process(event)
        if prom:
            prom.stats(reporter)

