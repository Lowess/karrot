#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""WSGI callable."""

from karrot import create_app
import gunicorn.app.wsgiapp as wsgi


def worker_exit(server, worker):
    from prometheus_client import multiprocess
    multiprocess.mark_process_dead(worker.pid)


preload_app = True

wsgi.run()
