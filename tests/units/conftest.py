#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import os
from karrot import create_app
import json
import logging

SAMPLES_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../samples")

logger = logging.getLogger()


@pytest.fixture
def events(datafiles):
    e = []
    for event_file in os.listdir(SAMPLES_DIR):
        fullpath_event_file = os.path.join(os.path.realpath(SAMPLES_DIR), event_file)
        logger.info(fullpath_event_file)
        with open(fullpath_event_file) as json_event:
            e.append(json.load(json_event))
    return e


@pytest.fixture
def app():
    app = create_app()
    # app.config["KARROT_CLOUDWATCH_INTERVAL"] = 1
    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    yield app


@pytest.fixture(scope="function")
def prometheus(tmpdir, monkeypatch):
    # Create the multiproc_dir folder required by Prometheus
    prometheus_multiproc_dir = tmpdir.mkdir(".prom")
    monkeypatch.setenv("prometheus_multiproc_dir", str(prometheus_multiproc_dir))
