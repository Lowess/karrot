# :carrot: Karrot - A Kafka lag reporter processing events from Burrow

---

### *Because [Karrot :carrot:]() help you move forward when you rely on [Burro :horse:](https://github.com/linkedin/Burrow)*

---

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

Made with ♥ by GumGum engineers
