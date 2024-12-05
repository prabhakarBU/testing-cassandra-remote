CREATE KEYSPACE IF NOT EXISTS test_keyspace WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
USE test_keyspace;
CREATE TABLE IF NOT EXISTS stocks (
    stock_id UUID PRIMARY KEY,
    symbol TEXT,
    price FLOAT,
    timestamp TIMESTAMP
);
INSERT INTO stocks (stock_id, symbol, price, timestamp) 
VALUES (uuid(), 'DATASNAKE', 1550.50, toTimestamp(now()))
IF NOT EXISTS;
