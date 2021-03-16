
from kafka import KafkaProducer,KafkaConsumer
import json
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

def get_producer_config():
    logging.info("Creating producer object ..")

    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                             value_serializer=lambda x:
                             json.dumps(x).encode('utf-8'))
    print(producer.config)
    return producer


def get_consumer_events(topic):
    logging.info("Creating Consumer Object ..")
    consumer = KafkaConsumer(topic,
                             group_id='my-group',
                             value_deserializer=lambda m: json.loads(m.decode('ascii')),
                             bootstrap_servers=['localhost:9092'],
                             consumer_timeout_ms=10000)
    return consumer



