import time

import pika

from src.common.config import Config


class Publisher:
    def __init__(self):
        self.config = Config()
        self.connection = None
        self.channel = None

    def connect(self):
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
        self._setup_exchange()

    def _setup_exchange(self):
        self.channel.exchange_declare(
            exchange=self.config.EXCHANGE_NAME,
            exchange_type='fanout',
            durable=True
        )

    def publish(self, message):
        self.channel.basic_publish(
            exchange=self.config.EXCHANGE_NAME,
            routing_key='',
            body=message.encode(),
            properties=pika.BasicProperties(
                delivery_mode=2
            )
        )

    def run(self):
        try:
            self.connect()
            with open('/app/input.txt', 'r') as f:
                while True:
                    line = f.readline()
                    if not line:
                        time.sleep(2)
                        f.seek(0)
                        continue

                    self.publish(line.strip())
                    print(f"[PUB] Sent: {line.strip()}")
                    time.sleep(0.1)
        except Exception as e:
            print(f"Error: {str(e)}")
        finally:
            if self.connection:
                self.connection.close()


if __name__ == "__main__":
    Publisher().run()
