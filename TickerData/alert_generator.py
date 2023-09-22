from datetime import date as dt
import pandas as pd
import sqlalchemy
import json

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
    # compare price, ema, and sma
    for i in range(len(durations)):
        for idc in ['EMA', 'SMA']:
            if i==0:
                stock_data[f'Close>{idc}{durations[0]}'] = \
                        stock_data['Close'] > stock_data[f'{idc}{durations[0]}']
            else:
                stock_data[f'{idc}{durations[i-1]}>{idc}{durations[i]}'] = \
                        stock_data[f'{idc}{durations[i-1]}'] > stock_data[f'{idc}{durations[i]}']
        # stock_data[f'EMA{durations[i]}>SMA{durations[i]}'] = \
        #     stock_data[f'EMA{durations[i]}'] > stock_data[f'SMA{durations[i]}']
        
    # check for up or down trend. 
    cmp_cols = [c for c in stock_data.columns if ('>' in c) and ('Close' not in c)]
    trend_du = [d for d in durations if d >= 20]
    trend_cols = [c for c in cmp_cols for d in trend_du if str(d) in c]
    stock_data['up_trend'] = stock_data[trend_cols].all(axis=1)
    stock_data['down_trend'] = ~stock_data[trend_cols].any(axis=1)

    return stock_data
    
def alert_gen(stock_data, prev_trend=10):
    """Generate alert message"""
    change = stock_data.diff()
    alerts = stock_data[change.eq(True).any(axis=1)]
    date_diff = (dt.today() - alerts.iloc[-1]['Date']).days
    msg=[]
    if date_diff < 5:
        for c in alerts.columns[change.iloc[-1].eq(True)].tolist():
            last_alert_idx = alerts.index[-1]
            last_trunck = stock_data.iloc[last_alert_idx-prev_trend:last_alert_idx]
            if last_trunck['up_trend'].sum() > prev_trend*0.5 or \
                    last_trunck['down_trend'].sum() > prev_trend*0.5:
                msg.append(f"{c} = {alerts.iloc[-1][c]} on {alerts.iloc[-1]['Date']}")
        out_msg = '; '.join(msg)
    else:
        out_msg = None
    return out_msg

def trend_analysis(stock_data):
    """if all short ema > long ema, and short sma > long sma, trend up
    if  all short ema < long ema, and short sma < long sma, trend down,
    otherwise, trend unclear."""
    last_trunk = stock_data.iloc[-20:]
    num_up = last_trunk['up_trend'].sum()
    num_down = last_trunk['down_trend'].sum()

    return f"Trend was up for {num_up} days and down for {num_down} days in the last 20 days"
    # if closing price drop below ema5
    # if stock_data['Close'][]


symbols = ["AAPL", "GOOGL", "MSFT", "TEC.TO", "TSM", "ASML", "VSP.TO",
           "AMAT", "TLT", "TD", "RY", "V", "BMO", "CNR.TO", "ENB", "NTR", "NVDA",
           "ON", "TSLA", "TMF", "TD.TO", "BMO.TO", "NA.TO", "XOM", "PWR", "QQQ",
            "HGR", "GOLD", "CCO", "CADUSD", "JP1!" ]

# symbols = ["ASML"]

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
alerts = {s:{} for s in symbols}
for symbol in symbols:
    print(f"Analyze {symbol}")
    data = read_data(conn, symbol, '2000-01-01', dt.today().strftime('%Y-%m-%d'))
    if len(data)>1:
        data = process(data, [5, 10, 20, 60, 120])
        alerts[symbol]['alert'] = alert_gen(data, 10)
        alerts[symbol]['trend'] = trend_analysis(data)


print(json.dumps(alerts, indent=2))
# data.to_csv('test.csv')
# data[['Close', 'EMA20', 'SMA20', 'EMA60', 'SMA60', 'EMA120', 'SMA120']].iloc[-60:].plot()