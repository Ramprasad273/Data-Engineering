from kafka import KafkaConsumer
from kafka_configurations import get_consumer_events
import logging
import json


def consumer_with_auto_commit(topic):
    """
    Consumes messages from a specified Kafka topic and prints them to the console.

    This function creates a Kafka consumer that automatically commits offsets.
    It then listens for messages on the given topic and prints their content.

    Args:
        topic (str): The name of the Kafka topic to consume messages from.
    """
    #Create consumer object which consumes any message from the topic

    events = get_consumer_events(topic)
    print_messages(events)


def print_messages(events):
    """
    Iterates through a collection of Kafka messages and prints their details.

    For each message, it prints the topic, partition, offset, key, and value.

    Args:
        events (KafkaConsumer): A KafkaConsumer instance containing the messages to be printed.
    """
    # Iterate through the messages
    for message in events:
        # message value and key are raw bytes -- decode if necessary!
        # e.g., for unicode: `message.value.decode('utf-8')`
        print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                             message.offset, message.key,
                                             message.value))


if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    logging.info("Consumer app started")

    consumer_with_auto_commit("topic1")
    logging.info("consumer_with_auto_commit completed")
