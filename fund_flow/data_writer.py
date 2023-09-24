import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import sqlalchemy
from sqlalchemy import text

db_info = {'driver': 'ODBC Driver 17 for SQL Server',
            'server':'RyanPC' , 
            'database':'Ticker' ,
            'username': 'hl',
            'password': '123'} 

# Establish a connection to the SQL Server database
conn = sqlalchemy.create_engine('mssql+pyodbc://'+db_info['username']+':'+db_info['password']+\
                            '@' + db_info['server'] + \
                            '/' + db_info['database'] + \
                            '?driver=ODBC+Driver+17+for+SQL+Server')


# Function to check if a table exists in the database
def table_exists(conn, table_name):
    query = f"SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{table_name}'"
    result = conn.execute(query)
    return result.fetchone()[0] > 0


def get_latest_date(cursor, table_name):
    # Query the latest date for the given symbol
    query = f"SELECT MAX([Date]) FROM {table_name}"
    latest_date = cursor.execute(query)
    return latest_date.fetchone()[0]


def download_etfdb_fundflow(url):
    """Download fund flow data. Raw data are strings. """
    # Scrape the table from the URL
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')

    # Extract the table headers
    headers = [th.text for th in table.find_all('th')]
    headers = [h.split("\n\n")[1] for h in headers]
    for i in range(len(headers)):
        if headers[i]=="+/-":
            headers[i] = " ".join(headers[i-1:i+1])

    # Extract last updated date
    last_updated=""
    for p in soup.find_all("p"):
        if "Last updated" in p.text:
            last_updated = p.text
    publish_date = last_updated.split('Last updated on ')[1].strip("\n")
    publish_date = datetime.strptime(publish_date, '%b %d, %Y').date()
    # Extract the table rows
    rows = []
    for tr in table.find_all('tr'):
        data = [td.text.strip() for td in tr.find_all('td')]
        if len(data) == len(headers):
            rows.append(data)
    df = pd.DataFrame(data=rows, columns=headers)
    df['Date'] = publish_date
    return df


def to_sql_table(table_name, df):
    """Insert df to SQL table. If table exists, append."""
    # Check if the table exists in the database
    if not table_exists(conn, table_name):
        df.to_sql(table_name, conn, if_exists='replace')
        print("Database doesn't exists. Create and write data")
    elif publish_date > get_latest_date(conn, table_name):
        df.to_sql(table_name, conn, if_exists='append')
        print("Append data")
    else:
        print("Already up to date. ")


def convert_to_num(df):
    """Convert downloaded etf table from string to number.
    Specifically, convert 
        - '$xx,xxx.xx' to float. 
        - 'xx%' to float. 
        - 'xx.xx' to float.
    If a cell is not convertable, replace it with NaN. 
    Date and Names columns are skipped. """
    str_cols = ['Industry', 'Date', 'power_ranking_sort_text']
    remove_dollar = lambda x: pd.to_numeric(x.replace('$', '').replace(',', ''), errors='ignore')
    remove_pct = lambda x: pd.to_numeric(x.replace('%',''), errors='ignore')
    for col in df.columns:
        if col not in str_cols:
            
            if isinstance(df[col][0], str):
                if '$' in df[col][0]:
                    df[col] = df[col].apply(remove_dollar)
                elif '%' in df[col][0]:
                    df[col] = df[col].apply(remove_pct)
                else:
                    df[col] = df[col].apply(pd.to_numeric, errors='coerce')
    return df


if __name__ == "__main__":
    url = "https://etfdb.com/etfs/industry/"
    raw_df = download_etfdb_fundflow(url)
    to_sql_table('etf_fund_flow', raw_df)
    df = convert_to_num(raw_df)
    to_sql_table("etf_fund_flow_num", df)