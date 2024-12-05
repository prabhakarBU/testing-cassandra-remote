import polars as pl
from io import StringIO
import datetime
time_now  = datetime.datetime.now().strftime('%m_%d_%Y_%H_%M_%S') 

# Sample Polars DataFrame
df = pl.DataFrame({
    "Ticker": ["BTC", "ETH", "XRP"],
    "Month": ["2024-01", "2024-01", "2024-01"],
    "Gain": [5.6, 8.2, 3.1]
})

# Convert Polars DataFrame to a string
output = StringIO()
path = "write-test.csv" + time_now
df.write_csv(path, include_header=True, separator=",")
df_str = output.getvalue().strip()  # Retrieve and strip CSV string

# Print result
print(df_str)
