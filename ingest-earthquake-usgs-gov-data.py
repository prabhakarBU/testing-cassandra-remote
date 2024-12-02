import os
import yfinance as yf
import polars as pl
from datetime import datetime
from cassandra.cluster import Cluster

# Define a function to fetch data
def fetch_trade_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    df = pl.DataFrame(stock_data.reset_index())
    return df


# Main function for data ingestion and saving to Delta
def main():
    # Fetch example data for a specific stock
    ticker = "AAPL"
    start_date = "2024-11-01"
    end_date = datetime.now().strftime("%Y-%m-%d")

    print("start reading: ")
    print(datetime.now())
    data = fetch_trade_data(ticker, start_date, end_date)
    print(data)
    print("End reading >> Start Writing: ")
    print(datetime.now())
    # print(data)
    # Connect to Cassandra
    # cluster = Cluster(['127.0.0.1'])
    # session = cluster.connect('stock_data')
    # # Insert raw data
    # session.execute("""
    # INSERT INTO raw_data (ticker, date, metric, value)
    # VALUES ('AAPL', '2024-01-01', 'rolling_7d_mean', 150.25)
    # """)
    # session.execute("""
    # INSERT INTO summarized_data (ticker, date, metric, value)
    # VALUES ('AAPL', '2024-01-02', 'rolling_7d_mean', 151.33)
    # """)
    

if __name__ == "__main__":
    main()
