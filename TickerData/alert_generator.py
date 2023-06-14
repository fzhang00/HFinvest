import pyodbc
from datetime import date as dt
import pandas as pd

def read_data(cursor, symbol : str, start : str, end : str):
    """Get ticker historical data from start state to end date"""
    # Retrieve ticker data for the given symbol, start date, and end date
    query = f"SELECT [Date], [Open], [High], [Low], [Close], [Volume] FROM StockData " \
            f"WHERE Symbol='{symbol}' AND Date >= '{start}' AND Date <= '{end}' " \
            f"ORDER BY Date"
    cursor.execute(query)
    ticker_data = cursor.fetchall()

    return ticker_data

def calculate_moving_high_low(stock_data, durations : list):
    """Calculate moving high low"""
    for d in durations:
        # Calculate the moving high and low prices
        stock_data[f'MovingHigh_{d}'] = stock_data['High'].rolling(d).max()
        stock_data[f'MovingLow5_{d}'] = stock_data['Low'].rolling(d).min()

    return stock_data

def calculate_ema(stock_data, durations : list):
    """Calculate ema, add result to dataframe"""
    for d in durations:
        stock_data[f'EMA{d}'] = stock_data['Close'].ewm(span=5, adjust=False).mean()

    return stock_data

def calculate_sma(stock_data, durations : list):
    """Calculate sma, add result to dataframe"""
    for d in durations:
        stock_data[f'EMA{d}'] = stock_data['Close'].rolling(window=5).mean()

    return stock_data    

def trend_analysis(stock_data):
    """Generete analysis columns"""
    pass
def alert_gen(stock_data):
    """Generate alert message"""
    msg = ''
    pass

symbols = ['TEC.TO']
# Connect to the MS SQL Server
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=;DATABASE=TickerData;UID=;PWD=')

# Create a cursor to execute SQL queries
cursor = conn.cursor()
for symbol in symbols:
    data = read_data(cursor, symbol, '2023-01-01', dt.today().strftime('%Y-%m-%d'))
    data = calculate_moving_high_low(data, [5, 10, 20])
    data = calculate_ema(data, [5, 10, 20])
    data = calculate_sma(data, [5, 10, 20])