from datetime import date as dt
import pandas as pd
import sqlalchemy

RYAN_SQL = {'driver': 'ODBC Driver 17 for SQL Server',
            'server':'RyanPC' , 
            'database':'Commodity_A1' ,
            'username': 'hl',
            'password': '123'} 

def read_data(conn, symbol : str, start : str, end : str):
    """Get ticker historical data from start state to end date"""
    # Retrieve ticker data for the given symbol, start date, and end date
    query = f"SELECT [Date], [Open], [High], [Low], [Close], [Volume] FROM StockData " \
            f"WHERE Symbol='{symbol}' AND Date >= '{start}' AND Date <= '{end}' " \
            f"ORDER BY Date"
    # cursor.execute(query)
    ticker_data = pd.read_sql(query, conn)

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
        stock_data[f'EMA{d}'] = stock_data['Close'].ewm(span=d, adjust=False).mean()

    return stock_data

def calculate_sma(stock_data, durations : list):
    """Calculate sma, add result to dataframe"""
    for d in durations:
        stock_data[f'SMA{d}'] = stock_data['Close'].rolling(window=d).mean()

    return stock_data    

def process(stock_data, durations):
    durations.sort()
    stock_data = calculate_moving_high_low(stock_data, durations)
    stock_data = calculate_ema(stock_data, durations)
    stock_data = calculate_sma(stock_data, durations)
    for i in range(len(durations)):
        for idc in ['EMA', 'SMA']:
            if i==0:
                stock_data[f'Close>{idc}{durations[0]}'] = \
                        stock_data['Close'] > stock_data[f'{idc}{durations[0]}']
            else:
                stock_data[f'{idc}{durations[i-1]}>{idc}{durations[i]}'] = \
                        stock_data[f'{idc}{durations[i-1]}'] > stock_data[f'{idc}{durations[i]}']
    return stock_data

def trend_analysis(stock_data):
    """Generete analysis columns"""
    pass
def alert_gen(stock_data):
    """Generate alert message"""
    change = stock_data.diff()
    alerts = stock_data[change.eq(True).any(axis=1)]
    date_diff = (dt.today() - alerts.iloc[-1]['Date']).days
    if date_diff < 5:
        print("generate alert for ")


    msg = ''
    # if closing price drop below ema5
    # if stock_data['Close'][]


symbols = ['TEC.TO']
db_info = RYAN_SQL
db_info['database'] = "Ticker"
# Connect to the MS SQL Server
# conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=;DATABASE=TickerData;UID=;PWD=')
conn = sqlalchemy.create_engine('mssql+pyodbc://'+db_info['username']+':'+db_info['password']+\
                            '@' + db_info['server'] + \
                            '/' + db_info['database'] + \
                            '?driver=ODBC+Driver+17+for+SQL+Server')
# Create a cursor to execute SQL queries
# cursor = conn.cursor()
for symbol in symbols:
    data = read_data(conn, symbol, '2023-01-01', dt.today().strftime('%Y-%m-%d'))
    data = process(data, [5, 10, 20])
    alert_gen(data)
data.to_csv('test.csv')
data.plot()