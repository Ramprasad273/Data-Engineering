# Kafka 101: Producer and Consumer

Foundational stream processing implementation demonstrating Apache Kafka message publishing, key-based partitioning, consumer group offset commits, and JSON serialization in Python.

## Architecture

```
┌───────────────────┐               ┌───────────────────┐               ┌───────────────────┐
│ kafka_producer.py │ ────(send)──> │   Kafka Broker    │ <──(consume)─ │ kafka_consumer.py │
└───────────────────┘               │  (Topic: topic1)  │               └───────────────────┘
                                    └───────────────────┘
                                              ▲
                                              │ (config & serializers)
                                    ┌─────────────────────────┐
                                    │ kafka_configurations.py │
                                    └─────────────────────────┘
```

### Components

- `kafka_producer.py`: Publishes structured JSON events to `topic1`, demonstrating both round-robin and key-based hashed partitioning.
- `kafka_consumer.py`: Subscribes to `topic1` under consumer group `my-group`, deserializes UTF-8 JSON payloads, and logs message metadata.
- `kafka_configurations.py`: Centralized configuration provider with environment variable overrides (`KAFKA_BOOTSTRAP_SERVERS`) and UTF-8 JSON serializers/deserializers.

## Execution Guide

### 1. Prerequisites
- Python 3.10+
- Running Kafka broker (local or containerized)

Install dependencies:
```bash
pip install kafka-python
```

To run a quick local Kafka broker using Docker (KRaft mode, no ZooKeeper required):
```bash
docker run -d --name kafka-broker \
  -p 9092:9092 \
  -e KAFKA_NODE_ID=1 \
  -e KAFKA_PROCESS_ROLES=broker,controller \
  -e KAFKA_LISTENERS=PLAINTEXT://:9092,CONTROLLER://:9093 \
  -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092 \
  -e KAFKA_CONTROLLER_LISTENER_NAMES=CONTROLLER \
  -e KAFKA_CONTROLLER_QUORUM_VOTERS=1@localhost:9093 \
  -e KAFKA_INTER_BROKER_LISTENER_NAME=PLAINTEXT \
  -e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 \
  apache/kafka:latest
```

### 2. Start the Consumer
In a terminal, start the consumer listener:
```bash
python kafka_consumer.py
```
The consumer will listen for events on `topic1`.

### 3. Publish Events via Producer
In a second terminal, execute the producer:
```bash
python kafka_producer.py
```

### 4. Verify Message Ingestion
The consumer console will output received records along with partition and offset metadata:
```text
topic1:0:0: key=None value={'App': 'Producer 1'}
topic1:0:1: key=b'client1' value={'App': 'Producer 2'}
```

## Configuration

The scripts support the `KAFKA_BOOTSTRAP_SERVERS` environment variable for remote or containerized broker connectivity:
```bash
export KAFKA_BOOTSTRAP_SERVERS="kafka-broker:9092"
python kafka_consumer.py
```

## Troubleshooting

- `kafka.errors.NoBrokersAvailable`: The client cannot reach the Kafka broker at the configured address. Confirm the broker is running and port 9092 is exposed.
- `ModuleNotFoundError: No module named 'kafka'`: Run `pip install kafka-python`.
- Partition distribution: Messages published with explicit partition keys (`client1`) are hashed to the same partition, guaranteeing ordered processing for the key.