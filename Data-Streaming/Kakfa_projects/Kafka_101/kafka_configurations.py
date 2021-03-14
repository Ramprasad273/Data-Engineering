
from kafka import KafkaProducer
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


