"""
Sample code consuming messages from a Kafka topic with auto-commit.
"""

import logging
from kafka_configurations import get_consumer_events


def consumer_with_auto_commit(topic):
    """
    Consumes messages from a specified Kafka topic and prints them to the console.

    Args:
        topic (str): The name of the Kafka topic to consume messages from.
    """
    events = get_consumer_events(topic)
    print_messages(events)


def print_messages(events):
    """
    Iterates through a collection of Kafka messages and prints their details.

    Args:
        events (KafkaConsumer): A KafkaConsumer instance containing the messages to be printed.
    """
    for message in events:
        print(f"{message.topic}:{message.partition}:{message.offset}: key={message.key} value={message.value}")


if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    logging.info("Consumer app started")

    consumer_with_auto_commit("topic1")
    logging.info("consumer_with_auto_commit completed")
