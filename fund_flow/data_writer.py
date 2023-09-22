import requests
from bs4 import BeautifulSoup
import pyodbc
from datetime import datetime
import pandas as pd
import sqlalchemy
from sqlalchemy import text

db_info = {'driver': 'ODBC Driver 17 for SQL Server',
            'server':'RyanPC' , 
            'database':'Ticker' ,
            'username': 'hl',
            'password': '123'} 
# URL of the webpage with the table
url = 'https://etfdb.com/etfs/industry/#industry-power-rankings__fund-flow-leaderboard&sort_name=aum_position&sort_order=asc&page=1'

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
    query = f"SELECT MAX([Date]) FROM etf_fund_flow"
    latest_date = cursor.execute(query)
    return latest_date.fetchone()[0]


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

# Specify the table name
table_name = 'etf_fund_flow'


# Check if the table exists in the database
if not table_exists(conn, table_name):
    df.to_sql(table_name, conn, if_exists='replace')
    print("Database doesn't exists. Create and write data")
elif publish_date > get_latest_date(conn, table_name):
    df.to_sql(table_name, conn, if_exists='append')
    print("Append data")
else:
    print("Already up to date. ")
