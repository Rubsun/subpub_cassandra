import sys
import time

import pika

from src.common.config import Config
from src.common.database import Database


class Consumer:
    def __init__(self, table_name):
        self.config = Config()
        self.table = table_name
        self.db = Database(table_name)
        self._connect_rabbitmq()

    def _connect_rabbitmq(self):
        credentials = pika.PlainCredentials(
            self.config.RABBIT_USER,
            self.config.RABBIT_PASSWORD
        )
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.config.RABBIT_HOST,
                credentials=credentials
            )
        )
        self.channel = self.connection.channel()

        self.channel.exchange_declare(
            exchange=self.config.EXCHANGE_NAME,
            exchange_type='fanout',
            durable=True
        )

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.queue_name = result.method.queue
        self.channel.queue_bind(
            exchange=self.config.EXCHANGE_NAME,
            queue=self.queue_name
        )

    def _process_message(self, ch, method, properties, body):
        try:
            message = body.decode()
            print(f"[CONS] Processing: {message}")
            self.db.save_message(message)
            time.sleep(0.2)
        finally:
            ch.basic_ack(delivery_tag=method.delivery_tag)

    def start(self):
        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=self._process_message
        )
        print("Consumer started. Waiting for messages...")
        self.channel.start_consuming()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: consumer.py <table_name>")
        sys.exit(1)
    Consumer(sys.argv[1]).start()
