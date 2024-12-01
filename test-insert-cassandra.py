from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from uuid import uuid4
import datetime

# Connect to the Cassandra cluster
cluster = Cluster(['127.0.0.1'], port=9042)  # Replace with container's IP if needed
session = cluster.connect()

# Use the keyspace
session.set_keyspace('test_keyspace')

# Insert data
insert_query = """
    INSERT INTO stocks (stock_id, symbol, price, timestamp)
    VALUES (%s, %s, %s, %s);
"""

# Example data to insert
data = [
    (uuid4(), 'AAPL', 150.75, datetime.datetime.now()),
    (uuid4(), 'MSFT', 299.65, datetime.datetime.now()),
    (uuid4(), 'GOOG', 2729.89, datetime.datetime.now())
]

for row in data:
    session.execute(insert_query, row)

print("Data inserted successfully!")

# Fetch and display the data
rows = session.execute('SELECT * FROM stocks;')
for row in rows:
    print(row)

# Close the connection
cluster.shutdown()
