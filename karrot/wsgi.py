#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""WSGI callable."""

from karrot import create_app  # noqa: F401
from prometheus_client import multiprocess
import logging
import shutil
import os

logger = logging.getLogger(__name__)


def on_reload(server):
    prom_dir = os.getenv("prometheus_multiproc_dir", None)
    if prom_dir is not None:
        logger.info(f"Flushing out Prometheus multiproc directory: {prom_dir}/*")

        for root, dirs, files in os.walk(prom_dir):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))

    else:
        raise RuntimeError("You must set `prometheus_multiproc_dir=<directory>`")


def child_exit(server, worker):
    logger.warning(f"{worker} died. marking process as dead in Prometheus registry")
    multiprocess.mark_process_dead(worker.pid)


preload_app = True
bind = "0.0.0.0:5000"
workers = 4
loglevel = "info"
