#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import current_app as app

def prometheus_prefix(name):
    return "{}_{}".format(app.config["KARROT_PROMETHEUS_METRIC_PREFIX"],
                          name)
