import polars as pl
from io import StringIO

# Sample Polars DataFrame
df = pl.DataFrame({
    "Ticker": ["BTC", "ETH", "XRP"],
    "Month": ["2024-01", "2024-01", "2024-01"],
    "Gain": [5.6, 8.2, 3.1]
})

# Convert Polars DataFrame to a string
output = StringIO()
df.write_csv(output, has_header=True, sep=",")
df_str = output.getvalue().strip()  # Retrieve and strip CSV string

# Print result
print(df_str)
