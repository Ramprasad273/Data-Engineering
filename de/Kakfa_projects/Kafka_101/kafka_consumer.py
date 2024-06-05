from kafka import KafkaConsumer
from kafka_configurations import get_consumer_events
import logging
import json


def consumer_with_auto_commit(topic):
    """

    :param topic: Topic to consume message from
    :return:
    """
    #Create consumer object which consumes any message from the topic

    events = get_consumer_events(topic)
    print_messages(events)


def print_messages(events):
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
