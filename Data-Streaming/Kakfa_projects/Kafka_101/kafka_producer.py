"""
This file contains the sample code which publishes message to the Kafka brokers.
"""

# Import all the required packages
import logging
from kafka import KafkaProducer
from kafka_configurations import get_producer_config


# produce json messages
def publish_message(producer,topic,message):
    logging.info("Publish json messages to topic")
    producer.send(topic, message)


def publish_message_with_key(producer,topic,key,message):
    logging.info("Publish json messages with key to topic")
    producer.send(topic, key=key, value=message)


if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    logging.info("Starting the Producer Application")
    logging.info("Create the producer object")
    producer = get_producer_config()
    event = {"App":"Producer 1"}
    event_1 = {"App": "Producer 2"}

    #Publish message to a topic
    publish_message(get_producer_config(),"topic1",event)

    #Publish message to a topic with key to enable hashed partitioning
    publish_message_with_key(get_producer_config(),"topic2",b"client1",event_1)


    # block until all async messages are sent
    producer.flush()





