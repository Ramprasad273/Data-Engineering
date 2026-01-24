
from kafka import KafkaProducer,KafkaConsumer
import json
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


def get_producer_config():
    """
    Creates and returns a Kafka producer instance.

    The producer is configured to connect to a Kafka broker on localhost:9092 and
    serialize message values as JSON.

    Returns:
        KafkaProducer: An instance of the Kafka producer.
    """
    logging.info("Creating producer object ..")
    # The Producer object requires the Kafka server, Json serializer
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                             value_serializer=lambda x:
                             json.dumps(x).encode('utf-8'))
    print(producer.config)
    return producer


def get_consumer_events(topic):
    """
    Creates and returns a Kafka consumer instance for a given topic.

    The consumer is configured to connect to a Kafka broker on localhost:9092,
    belong to the 'my-group' consumer group, and deserialize JSON messages.
    It will time out after 10 seconds if no new messages are received.

    Args:
        topic (str): The name of the Kafka topic to consume from.

    Returns:
        KafkaConsumer: An instance of the Kafka consumer.
    """
    logging.info("Creating Consumer Object ..")
    # The consumer object contains the topic name, json deserializer,Kafka servers
    # and kafka time out in ms, Stops the iteration if no message after 1 sec
    consumer = KafkaConsumer(topic,
                             group_id='my-group',
                             value_deserializer=lambda m: json.loads(m.decode('ascii')),
                             bootstrap_servers=['localhost:9092'],
                             consumer_timeout_ms=10000)
    return consumer



