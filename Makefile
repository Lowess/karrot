.PHONY: dev tests lint checkstyle coverage docs run gunicorn docker
SHELL := /bin/bash

docker:
	docker build . -t lowess/karrot

docker-run:
	docker run -it --rm \
	--name karrot \
	-v ~/.aws:/root/.aws \
	-p 5000:5000 \
	lowess/karrot

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
	rm -rf .prom; mkdir -p .prom; \
	export prometheus_multiproc_dir=.prom; \
	export FLASK_APP=karrot; \
	export FLASK_ENV=dev; \
	flask run

gunicorn:
	@echo 🚀 Run production gunicorn...
	rm -rf .prom; mkdir -p .prom; \
	export prometheus_multiproc_dir=.prom; \
	export FLASK_APP=karrot.wsgi; \
	export FLASK_ENV=prod; \
	gunicorn 'karrot:create_app()' --config karrot/wsgi.py
