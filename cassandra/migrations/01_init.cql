CREATE KEYSPACE IF NOT EXISTS pubsub_data
WITH REPLICATION = {
    'class' : 'NetworkTopologyStrategy',
    'replication_factor' : 1
};

CREATE TABLE IF NOT EXISTS pubsub_data.processed_alpha (
    message_id timeuuid PRIMARY KEY,
    content text,
    processed_at timestamp
);

CREATE TABLE IF NOT EXISTS pubsub_data.processed_beta (
    message_id timeuuid PRIMARY KEY,
    content text,
    processed_at timestamp
);