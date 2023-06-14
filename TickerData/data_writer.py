import yfinance as yf
import pyodbc
from datetime import date as dt

# Define the list of symbols
symbols = ["AAPL", "GOOGL", "MSFT", "TEC.TO", "TSM", "ASML"]

def insert_data(cursor, symbol: str, start: str, end: str):
    # Download historical data using yfinance
    data = yf.download(symbol, start=start, end=end)

    # Iterate through each row of data and insert new records into the database
    for index, row in data.iterrows():
        date = index.strftime('%Y-%m-%d')
        open_price = row['Open']
        high_price = row['High']
        low_price = row['Low']
        close_price = row['Close']
        volume = row['Volume']

        # Check if the data point already exists in the database
        query = f"SELECT COUNT(*) FROM StockData WHERE [Symbol]='{symbol}' AND [Date]='{date}'"
        cursor.execute(query)
        count = cursor.fetchone()[0]

        # If the data point doesn't exist, insert it into the database
        if count == 0:
            insert_query = f"INSERT INTO StockData ([Symbol], [Date], [Open], [High], [Low], [Close], [Volume]) " \
                           f"VALUES ('{symbol}', '{date}', {open_price}, {high_price}, {low_price}, {close_price}, {volume})"
            cursor.execute(insert_query)


def get_latest_date(cursor, symbol):
    # Query the latest date for the given symbol
    query = f"SELECT MAX([Date]) FROM StockData WHERE [Symbol]='{symbol}'"
    cursor.execute(query)
    latest_date = cursor.fetchone()[0]

    return latest_date

# Function to check if table exists
def table_exists(table_name):
    query = f"SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{table_name}'"
    cursor.execute(query)
    count = cursor.fetchone()[0]
    print(f"Table exist {count}")
    return count > 0

def create_table(cursor, table_name):
    # Check if table exists, if not, create the table
    if not table_exists(table_name):
        create_table_query = """
        CREATE TABLE StockData (
            [Symbol] VARCHAR(10),
            [Date] DATE,
            [Open] DECIMAL(12, 2),
            [High] DECIMAL(12, 2),
            [Low] DECIMAL(12, 2),
            [Close] DECIMAL(12, 2),
            [Volume] BIGINT
        )
        """
        cursor.execute(create_table_query)
        conn.commit()



# Connect to the MS SQL Server
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=;DATABASE=TickerData;UID=;PWD=')

# Create a cursor to execute SQL queries
cursor = conn.cursor()
create_table(cursor, "StockData")
# Loop through each symbol and download historical data
for symbol in symbols:
    latest_date = get_latest_date(cursor, symbol)
    print(symbol, latest_date)
    if latest_date is None: # symbol doesn't exists
        latest_date = "1970-01-01"
    insert_data(cursor, symbol, latest_date, dt.today().strftime("%Y-%m-%d"))
    # Commit the changes for each symbol
    conn.commit()

# Close the database connection
conn.close()
