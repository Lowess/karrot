.PHONY: run gunicorn
SHELL := /bin/bash


run:
	export prometheus_multiproc_dir=.prom; \
	export FLASK_APP=karrot; \
	export FLASK_DEV=dev; \
	flask run

gunicorn:
	export prometheus_multiproc_dir=.prom; \
	export FLASK_APP=karrot.wsgi; \
	export FLASK_DEV=prod; \
	flask "karrot:create_app()" --bind 127.0.0.1:5000 -w 1
