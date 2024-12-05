from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from uuid import uuid4
import boto3
import datetime
import polars as pl
import os
time_now  = datetime.datetime.now().strftime('%m_%d_%Y_%H_%M_%S') 

# Connect to the Cassandra cluster
USERNAME = "cassandra"
PASSWORD = "cassandra"
auth_provider = PlainTextAuthProvider(USERNAME, PASSWORD)
cluster = Cluster(['127.0.0.1'], auth_provider=auth_provider)  # Replace with container's IP if needed
session = cluster.connect()


# Use the keyspace
session.set_keyspace('test_keyspace')

# Insert data
insert_query = """
    INSERT INTO stocks (stock_id, symbol, price, timestamp)
    VALUES (%s, %s, %s, %s);
"""

# Example data to insert
# data = [
#     (uuid4(), 'AAPL', 150.75, datetime.datetime.now()),
#     (uuid4(), 'MSFT', 299.65, datetime.datetime.now()),
#     (uuid4(), 'GOOG', 2729.89, datetime.datetime.now())
# ]

# Create a Polars DataFrame with example data
data_frame = pl.DataFrame({
    "stock_id": [str(uuid4()) for _ in range(3)],
    "symbol": ["AAPL", "MSFT", "GOOG"],
    "price": [150.75, 299.65, 2729.89],
    "timestamp": [datetime.datetime.now() for _ in range(3)]
})

print("Printing Polars data frame:")
print(data_frame)


for row in data_frame.iter_rows(named=True):
    session.execute(insert_query, (row["stock_id"], row["symbol"], row["price"], row["timestamp"]))
    
# for row in data:
    # session.execute(insert_query, row)

print("Data inserted successfully to Cassandra!")

# Update a record
# update_query = """
#     UPDATE stocks 
#     SET price = %s 
#     WHERE stock_id = %s;
# """

# Example: Updating the price of the first record
# stock_id_to_update = 'f46905bd-7763-4aff-bb8c-9d2a4f3ceced' # data[0][0]  # UUID of the first record
# new_price = 155.55
# session.execute(update_query, (new_price, stock_id_to_update))

# print(f"Updated stock_id {stock_id_to_update} to price {new_price}")

# Verify the update
# select_query = "SELECT * FROM stocks WHERE stock_id = %s;"
# result = session.execute(select_query, (stock_id_to_update,))
# for row in result:
#     print("Updated record:", row)


# Fetch and display the data
rows = session.execute('SELECT * FROM stocks;')
for row in rows:
    print(row)

# add to s3 bucket

# Save DataFrame as Parquet and CSV
output_dir = "./output-files"
os.makedirs(output_dir, exist_ok=True)
parquet_file_name = "stocks.parquet"+time_now
csv_file_name = "stocks.csv"+time_now
parquet_file = os.path.join(output_dir, parquet_file_name)
csv_file = os.path.join(output_dir, csv_file_name)

data_frame.write_parquet(parquet_file)
data_frame.write_csv(csv_file)

print(f"Saved Parquet file at {parquet_file}")
print(f"Saved CSV file at {csv_file}")

# Upload to S3 bucket
s3_client = boto3.client('s3')
bucket_name = "testing-cassandra-remote-bucket"
project_name = "testing-cassandra-remote"

parquet_s3_key = f"{output_dir}/stocks.parquet"
csv_s3_key = f"{output_dir}/stocks.csv"

try:
    s3_client.upload_file(parquet_file, bucket_name, parquet_s3_key)
    print(f"Uploaded Parquet to S3: {bucket_name}/{parquet_s3_key}")
    
    s3_client.upload_file(csv_file, bucket_name, csv_s3_key)
    print(f"Uploaded CSV to S3: {bucket_name}/{csv_s3_key}")
except Exception as e:
    print(f"Error uploading to S3: {e}")

# Close the connection
cluster.shutdown()
