.PHONY: dev tests lint checkstyle coverage docs run gunicorn
SHELL := /bin/bash

dev:
	@echo ⚙️ Setting up dev environment and dependencies...
	pip install -r dev/requirements.txt

tests:
	$(MAKE) lint
	$(MAKE) checkstyle
	$(MAKE) coverage

lint:
	@echo 💠 Linting code...
	tox -e lint

checkstyle:
	@echo ✅ Validating checkstyle...
	tox -e checkstyle

coverage:
	@echo 🔍️  Run test coverage...
	tox -e coverage

docs:
	@echo 📚 Generate documentation using sphinx...
	$(MAKE) -C ./docs/sphinx html

run:
	@echo 🚀 Run development server...
	export prometheus_multiproc_dir=.prom; \
	export FLASK_APP=karrot; \
	export FLASK_ENV=dev; \
	flask run

gunicorn:
	@echo 🚀 Run production gunicorn...
	export prometheus_multiproc_dir=.prom; \
	export FLASK_APP=karrot.wsgi; \
	export FLASK_ENV=prod; \
	flask "karrot:create_app()" --bind 127.0.0.1:5000 -w 1
