# :carrot: Karrot - A Kafka lag reporter processing events from Burrow

---

### *Because [Karrot :carrot:]() help you move forward when you rely on [Burro :horse:](https://github.com/linkedin/Burrow)*

---

[Karrot](https://github.com/Lowess/karrot) is [Flask Webapp](http://flask.palletsprojects.com/en/1.1.x/) that acts as a lag reporting tool able to parse [Burrow](https://github.com/linkedin/Burrow) (a monitoring companion for [Apache Kafka](http://kafka.apache.org)) http notifications. It offers [AWS CloudWatch](https://aws.amazon.com/cloudwatch/) lag reporting as well as a [Prometheus](https://prometheus.io/) metrics exporter.

![Karrot Infrastructure Diagram](docs/img/karrot-diagram.png)

### Getting Started

* Local Development with built-in Flask server (:warn: Do not use in prod!)

```bash
export FLASK_APP=karrot
export FLASK_DEV=development
flask run
```

* Run in production with `gunicorn`:

```bash
export FLASK_APP=karrot.wsgi
export FLASK_DEV=production
flask "karrot:create_app()" --bind 127.0.0.1:8001 -w 4
```

* Running a Kafka / Zk / Burrow / Karrot stack locally

```bash
# Start the stack locally using docker-compose
cd tests/
docker-compose up

# Send messages to a test topic
docker exec -it \
  tests_kafka_1 \
  kafka-producer-perf-test.sh \
  --producer-props bootstrap.servers=localhost:9092 \
  --throughput 10 \
  --num-record 100000000 \
  --record-size 100 \
  --topic topicA

# Run a consumer polling from the test topic
docker exec -it \
   tests_kafka_1 \
   kafka-console-consumer.sh \
   --bootstrap-server kafka:9092 \
   --topic topicA \
   --from-beginning \
   --group topicA-consumer
```

# Karrot Environment variables

## Global Karrot env vars:

| env                | value                   | description                              |
|--------------------|-------------------------|------------------------------------------|
| `KARROT_LOG`       | `INFO, DEBUG, ERROR`    | The log level to use for the Karrot app  |
| `KARROT_REPORTERS` | `prometheus,cloudwatch` | A CSV list of reporters to use in Karrot |

## Reporter specific env vars:

| env                           | value                             | description                                                             |
|-------------------------------|-----------------------------------|-------------------------------------------------------------------------|
| `KARROT_CLOUDWATCH_NAMESPACE` | `GumGum/Kafka/Burrow/ConsumerLag` | The Cloudwatch namespace prefix to use for lag reporting                |
| `KARROT_CLOUDWATCH_INTERVAL`  | `30`                              | The Cloudwatch flush interval to execute the `put_metric_data` api call |

---

Made with ♥ by GumGum engineers
