#!/usr/bin/env bash

rm -rf /src/.prom; mkdir -p /src/.prom
export prometheus_multiproc_dir=/src/.prom

gunicorn $@
