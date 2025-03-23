import time

from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster

from src.common.config import Config


class Database:
    def __init__(self, table_name):
        self.config = Config()
        self.table = table_name

        auth_provider = PlainTextAuthProvider(
            username='cassandra',
            password='cassandra'
        )

        for _ in range(5):
            try:
                self.cluster = Cluster(
                    [self.config.CASSANDRA_HOST],
                    auth_provider=auth_provider
                )
                self.session = self.cluster.connect(self.config.KEYSPACE)
                break
            except Exception as e:
                print(f"Connection failed: {str(e)}, retrying...")
                time.sleep(5)
        else:
            raise RuntimeError("Failed to connect to Cassandra")

    def save_message(self, message):
        query = f"""
        INSERT INTO {self.table} 
        (message_id, content, processed_at)
        VALUES (now(), %s, toTimestamp(now()))
        """
        self.session.execute(query, (message,))
