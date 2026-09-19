"""
Sample code publishing messages to Kafka brokers with and without partition keys.
"""

import logging
from kafka_configurations import get_producer_config


def publish_message(producer, topic, message):
    """
    Publishes a message to a specified Kafka topic.

    Args:
        producer (KafkaProducer): The Kafka producer instance to use for sending the message.
        topic (str): The name of the topic to publish the message to.
        message (dict): The message to be published (will be JSON serialized).
    """
    logging.info("Publishing JSON message to topic: %s", topic)
    producer.send(topic, message)


def publish_message_with_key(producer, topic, key, message):
    """
    Publishes a message with a key to a specified Kafka topic.

    The key is used by Kafka for partitioning, ensuring that messages with the same key
    are sent to the same partition.

    Args:
        producer (KafkaProducer): The Kafka producer instance.
        topic (str): The name of the topic to publish to.
        key (bytes): The key for message partitioning.
        message (dict): The message to be published (will be JSON serialized).
    """
    logging.info("Publishing JSON message with key '%s' to topic: %s", key, topic)
    producer.send(topic, key=key, value=message)


if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    logging.info("Starting the Producer Application")

    producer = get_producer_config()
    logging.info("Producer created successfully")

    event = {"App": "Producer 1"}
    event_1 = {"App": "Producer 2"}

    # Publish message to a topic
    publish_message(producer, "topic1", event)

    # Publish message to a topic with key to enable hashed partitioning
    publish_message_with_key(producer, "topic1", b"client1", event_1)

    # Block until all async messages are sent
    producer.flush()
    logging.info("All messages successfully flushed")
