import json
import logging
import os
from kafka import KafkaConsumer, KafkaProducer

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

DEFAULT_BOOTSTRAP_SERVERS = [os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")]


def get_producer_config(bootstrap_servers=None):
    """
    Creates and returns a Kafka producer instance.

    The producer connects to the specified Kafka broker (defaulting to
    KAFKA_BOOTSTRAP_SERVERS or localhost:9092) and serializes message values as JSON (UTF-8).

    Returns:
        KafkaProducer: An instance of the Kafka producer.
    """
    servers = bootstrap_servers or DEFAULT_BOOTSTRAP_SERVERS
    logging.info("Creating Kafka producer connected to %s", servers)
    producer = KafkaProducer(
        bootstrap_servers=servers,
        value_serializer=lambda x: json.dumps(x).encode("utf-8"),
    )
    return producer


def get_consumer_events(topic, bootstrap_servers=None, group_id="my-group"):
    """
    Creates and returns a Kafka consumer instance for a given topic.

    The consumer connects to the specified Kafka broker, deserializes UTF-8 JSON
    messages, and times out after 10 seconds of inactivity.

    Args:
        topic (str): The name of the Kafka topic to consume from.
        bootstrap_servers (list, optional): List of Kafka broker addresses.
        group_id (str): Consumer group identifier.

    Returns:
        KafkaConsumer: An instance of the Kafka consumer.
    """
    servers = bootstrap_servers or DEFAULT_BOOTSTRAP_SERVERS
    logging.info("Creating Kafka consumer for topic '%s' on %s", topic, servers)
    consumer = KafkaConsumer(
        topic,
        group_id=group_id,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        bootstrap_servers=servers,
        consumer_timeout_ms=10000,
    )
    return consumer
