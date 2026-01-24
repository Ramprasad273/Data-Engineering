"""
This file contains the sample code which publishes message to the Kafka brokers.

1. publish_message function pushes the message to the topic
2. publish_message_with_key pushes the message with key

"""

# Import all the required packages
import logging
from kafka_configurations import get_producer_config


# Publish json messages
def publish_message(producer, topic, message):
    """
    Publishes a message to a specified Kafka topic.

    Args:
        producer (KafkaProducer): The Kafka producer instance to use for sending the message.
        topic (str): The name of the topic to publish the message to.
        message (dict): The message to be published (will be JSON serialized).
    """
    logging.info("Publish json messages to  ", str(topic))
    producer.send(topic, message)


# Publish json messages with key
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
    logging.info("Publish json messages with key to ", str(topic))
    producer.send(topic, key=key, value=message)


if __name__ == '__main__':

    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    logging.info("Starting the Producer Application")
    logging.info("Create the producer object")
    # Create the producer object with basic configurations
    producer = get_producer_config()
    logging.info("Producer metrics", producer.metrics())
    event = {"App": "Producer 1"}
    event_1 = {"App": "Producer 2"}

    # Publish message to a topic
    publish_message(producer, "topic1", event)

    # Publish message to a topic with key to enable hashed partitioning
    publish_message_with_key(producer, "topic1", b"client1", event_1)

    # block until all async messages are sent
    producer.flush()





