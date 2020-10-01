#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, Response
from prometheus_client import multiprocess
from prometheus_client import generate_latest, CollectorRegistry, CONTENT_TYPE_LATEST


# Define a blueprint
prometheus = Blueprint("prometheus", __name__, url_prefix="/metrics")


# http://<hostname>/metrics endpoint
@prometheus.route("", methods=["GET"])
def metrics():
    registry = CollectorRegistry()
    multiprocess.MultiProcessCollector(registry)
    data = generate_latest(registry)
    return Response(data, mimetype=CONTENT_TYPE_LATEST)
