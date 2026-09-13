import logging
import json
from copy import deepcopy

try:
    from kafka import KafkaProducer
    KAFKA_AVAILABLE = True
except ImportError:
    KAFKA_AVAILABLE = False

from airflow.config_templates.airflow_local_settings import DEFAULT_LOGGING_CONFIG

if KAFKA_AVAILABLE:
    class KafkaLogHandler(logging.Handler):
        def __init__(self, bootstrap_servers, topic):
            super().__init__()
            self.topic = topic
            # Initialize the Kafka producer
            self.producer = KafkaProducer(
                bootstrap_servers=bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )

        def emit(self, record):
            try:
                # Format the log record
                msg = self.format(record)
                log_data = {
                    'logger': record.name,
                    'level': record.levelname,
                    'message': msg,
                    'filename': record.filename,
                    'lineno': record.lineno,
                    'funcName': record.funcName,
                    'timestamp': record.created
                }
                # Send to Kafka
                self.producer.send(self.topic, value=log_data)
            except Exception:
                self.handleError(record)

# Create a deepcopy of the default configuration
LOGGING_CONFIG = deepcopy(DEFAULT_LOGGING_CONFIG)

if KAFKA_AVAILABLE:
    # Define our new handler
    LOGGING_CONFIG['handlers']['kafka_task'] = {
        'class': 'airflow_local_settings.KafkaLogHandler',
        'formatter': 'airflow',
        'bootstrap_servers': ['kafka:9092'],
        'topic': 'airflow_logs',
    }

    # Add the new handler to the task logger alongside the default 'task' handler
    if 'airflow.task' in LOGGING_CONFIG['loggers']:
        if 'handlers' in LOGGING_CONFIG['loggers']['airflow.task']:
            LOGGING_CONFIG['loggers']['airflow.task']['handlers'].append('kafka_task')
        else:
            LOGGING_CONFIG['loggers']['airflow.task']['handlers'] = ['task', 'kafka_task']
