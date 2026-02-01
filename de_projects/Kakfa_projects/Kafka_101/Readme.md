# Kafka 101: Producer and Consumer

## Objective

This project provides a simple, educational example of a Kafka producer and consumer implemented in Python. It is designed to demonstrate the fundamental concepts of Kafka, including producing messages to a topic and consuming them.

The main goals of this project are:
- To provide a clear and concise example of a Kafka producer and consumer.
- To illustrate how to configure a Kafka producer and consumer in Python.
- To serve as a starting point for building more complex Kafka-based applications.

## Architecture

The project consists of three main Python scripts that interact with a Kafka broker:

```
+-----------------+      +-----------------+      +------------------+
| kafka_producer.py |----->|  Kafka Broker   |<-----| kafka_consumer.py |
+-----------------+      | (Topic: topic1) |      +------------------+
                         +-----------------+
                                   ^
                                   |
                         +-------------------------+
                         | kafka_configurations.py |
                         +-------------------------+
```

### Components

-   `kafka_producer.py`: A Python script that acts as a Kafka producer. It sends messages to a Kafka topic named `topic1`.
-   `kafka_consumer.py`: A Python script that acts as a Kafka consumer. It subscribes to the `topic1` topic and prints the messages it receives.
-   `kafka_configurations.py`: A utility script that provides configuration details for both the producer and the consumer, such as the Kafka broker address and serialization settings.

## How to Run

### Prerequisites

-   Python 3
-   A running Kafka and Zookeeper instance. You can use a Docker image for a quick setup. For example, using the `bitnami/kafka` image:
    ```bash
    docker run -d --name zookeeper -p 2181:2181 -e ALLOW_ANONYMOUS_LOGIN=yes bitnami/zookeeper:latest
    docker run -d --name kafka -p 9092:9092 --link zookeeper:zookeeper -e KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181 -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092 -e ALLOW_PLAINTEXT_LISTENER=yes bitnami/kafka:latest
    ```
-   Install the required Python library:
    ```bash
    pip install kafka-python
    ```

### 1. Start the Consumer

Open a terminal and run the consumer script. It will wait for messages on `topic1`.

```bash
python kafka_consumer.py
```

### 2. Start the Producer

Open another terminal and run the producer script. It will send two messages to `topic1`.

```bash
python kafka_producer.py
```

### 3. Observe the Output

-   In the consumer's terminal, you should see the messages sent by the producer, along with their metadata (topic, partition, offset, key, value).
-   The producer script will exit after sending the messages.
-   The consumer script will time out and exit after 10 seconds of inactivity.

## Common Issues and Fixes

-   **Issue**: `kafka.errors.NoBrokersAvailable: NoBrokersAvailable`.
    -   **Fix**: This error means that the producer or consumer cannot connect to the Kafka broker.
        1.  Ensure that your Kafka and Zookeeper instances are running correctly.
        2.  Verify that the `bootstrap_servers` in `kafka_configurations.py` is set to the correct address of your Kafka broker (e.g., `'localhost:9092'`).
        3.  If you are running Kafka in Docker, make sure the port `9092` is correctly mapped to your host machine.

-   **Issue**: The consumer doesn't receive any messages.
    -   **Fix**:
        1.  Make sure you start the consumer *before* the producer.
        2.  Check that the topic name in `kafka_producer.py` and `kafka_consumer.py` is the same (`topic1`).
        3.  If your Kafka broker has topic auto-creation disabled, you might need to create the `topic1` topic manually before running the scripts.

-   **Issue**: `ModuleNotFoundError: No module named 'kafka'`.
    -   **Fix**: You need to install the `kafka-python` library. Run `pip install kafka-python`.