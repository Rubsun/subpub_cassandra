import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    RABBIT_HOST = os.getenv('RABBIT_HOST', 'rabbitmq')
    RABBIT_USER = os.getenv('RABBIT_USER', 'admin')
    RABBIT_PASSWORD = os.getenv('RABBIT_PASSWORD', 'secret')
    EXCHANGE_NAME = os.getenv('EXCHANGE_NAME', 'pubsub_exchange')

    CASSANDRA_HOST = os.getenv('CASSANDRA_HOST', 'cassandra')
    KEYSPACE = os.getenv('CASSANDRA_KEYSPACE', 'pubsub_data')
