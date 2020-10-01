[![Build Status](https://cloud.drone.io/api/badges/Lowess/karrot/status.svg)](https://cloud.drone.io/Lowess/karrot)
[![Coverage Status](https://coveralls.io/repos/github/Lowess/karrot/badge.svg?branch=master)](https://coveralls.io/github/Lowess/karrot?branch=master)
[![Code style: black](https://img.shields.io/badge/code%20style-black-black.svg)](https://github.com/psf/black)
[![Linter: flake8](https://img.shields.io/badge/linter-flake8-blue.svg)](http://flake8.pycqa.org/en/latest/)
[![Linter: tests](https://img.shields.io/badge/tests-tox-yellow.svg)](hhttps://tox.readthedocs.io/en/latest)
[![Documentation Status](https://readthedocs.org/projects/karrot/badge/?version=latest)](https://karrot.readthedocs.io/en/latest/?badge=latest)

# :carrot: Karrot - A Kafka lag reporter processing events from Burrow

---

### *Because [Karrot :carrot:](https://github.com/Lowess/karrot) help you move forward when you ride on [Burrow :horse:](https://github.com/linkedin/Burrow)*

---

[Karrot](https://github.com/Lowess/karrot) is [Flask Webapp](http://flask.palletsprojects.com/en/1.1.x/) that acts as a lag reporting tool able to parse [Burrow](https://github.com/linkedin/Burrow) (a monitoring companion for [Apache Kafka](http://kafka.apache.org)) http notifications. It offers [AWS CloudWatch](https://aws.amazon.com/cloudwatch/) lag reporting as well as a [Prometheus](https://prometheus.io/) metrics exporter.

If you want to read more about Karrot please go check this [Medium article](https://medium.com/gumgum-tech/karrot-kafka-lag-reporting-at-scale-b32061dcc604)

![Karrot Infrastructure Diagram](docs/img/karrot-diagram.png)

# :pushpin: Requirements

If `cloudwatch` reporter is used (which is enabled by default), you must run Karrot with credentials that have the following IAM permissions:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "cloudwatch:PutMetricData"
            ],
            "Resource": "*"
        }
    ]
}
```

---

# :rocket: Getting Started

* Docker

```bash
docker run -it --rm \
  --name karrot \
  -v ~/.aws:/root/.aws \
  lowess/karrot
```

* Kubernetes

```bash
# Add the Repository to Helm:
$ helm repo add lowess-helm https://lowess.github.io/helm-charts

# Install karrrot helm chart:
$ helm install lowess-helm/karrot
```

* Local Development with built-in Flask server (:warning: [Do not use in production!](https://flask.palletsprojects.com/en/1.1.x/deploying/))

```bash
export FLASK_APP=karrot
export FLASK_ENV=development
flask run
```

* Run in production with `gunicorn` (:white_check_mark: Valid for production usage):

```bash
export FLASK_APP=karrot.wsgi
export FLASK_ENV=production
flask "karrot:create_app()" --bind 127.0.0.1:5000 -w 4
```

---


# Karrot Environment Variables

## Global Karrot env vars:

| env                | value                   | description                              |
|--------------------|-------------------------|------------------------------------------|
| `KARROT_LOG`       | `INFO, DEBUG, ERROR`    | The log level to use for the Karrot app  |
| `KARROT_REPORTERS` | `prometheus,cloudwatch` | A CSV list of reporters to use in Karrot |

## Reporter specific env vars:

* Cloudwatch

| env                           | value                             | description                                                             |
|-------------------------------|-----------------------------------|-------------------------------------------------------------------------|
| `KARROT_CLOUDWATCH_NAMESPACE` | `GumGum/Kafka/Burrow/ConsumerLag` | The Cloudwatch namespace prefix to use for lag reporting                |
| `KARROT_CLOUDWATCH_INTERVAL`  | `30`                              | The Cloudwatch flush interval to execute the `put_metric_data` api call |

---

# :wrench: Developer Guide

## TL;DR

```bash
# Install development requirements
make dev

# Setup pre-commit hook locally
pre-commit install

# Run full tests
make tests

# Build Sphinx documentation locally
make docs
```

## IDE configuration

* VSCode `settings.json`

```json
{
  "python.linting.pylintEnabled": false,
  "python.linting.flake8Enabled": true,
  "python.linting.enabled": true,
  "python.formatting.provider": "black",
  "python.pythonPath": "~/.pyenv/versions/konnector/bin/python",
  "python.venvPath": "~/.pyenv/shims",
  "editor.formatOnPaste": false,
  "editor.formatOnSave": true
}
```

## Formatting & Linters

 The project uses [Flake8](http://flake8.pycqa.org/en/latest/) linter and [Black](https://black.readthedocs.io/en/latest/) autoformatter

## Tests

Tests are automated with [Tox](https://tox.readthedocs.io/en/latest/) and run with [Pytest](https://docs.pytest.org/en/latest/) suite. [Codecoverage](https://coverage.readthedocs.io/en/latest/) is also reported during test runs.

## Documentation

The documentation can be genered with [Sphinx](https://www.sphinx-doc.org/en/2.0/)

## Running a Kafka / Zk / Burrow / Karrot stack locally

```bash
# Start the stack locally using docker-compose
cd docker/
docker-compose up

# Send messages to a test topic
docker exec -it \
  docker_kafka_1 \
  kafka-producer-perf-test.sh \
  --producer-props bootstrap.servers=localhost:9092 \
  --throughput 10 \
  --num-record 100000000 \
  --record-size 100 \
  --topic topicA

# Run a consumer polling from the test topic
docker exec -it \
   docker_kafka_1 \
   kafka-console-consumer.sh \
   --bootstrap-server kafka:9092 \
   --topic topicA \
   --from-beginning \
   --group topicA-consumer
```

---

Made with ♥ by GumGum engineers
