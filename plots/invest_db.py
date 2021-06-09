"""
A set of functions and classes to store and read data from our investment database
"""


import pyodbc
import pandas as pd
import numpy as np
# import sp500Const as const
import sqlalchemy
from sqlalchemy import text, inspect
# from ..key import QUANDL_KEY, RYAN_SQL, FAN_SQL
import pandas_datareader as web

QUANDL_KEY = '_JyFt8HS_T8C4qsXBo68'

BEA_Key = "5FCFE8A8-1714-4DE1-9F49-E8AFA9BEFB93"

# ------ SQL server on Ryan's PC -----------
RYAN_SQL = {'server':'RyanPC' , 
            'database':'Commodity_A1' ,
            'username': 'fz',
            'password': '123'} 
FAN_SQL = {'server':'DESKTOP-45300G7',
                'database':"Investment",
                'username':"hliu",
                'password':"123"}


class InvestDB():
    def __init__(self, db_info):
        """Create connection engine to investment database
        Input: 
            db_info: A dictionary with {'server':, 'username':, 'password':, 'database':}
        """
        self.sqlcon = sqlalchemy.create_engine('mssql+pyodbc://'+db_info['username']+':'+db_info['password']+\
                            '@' + db_info['server'] + \
                            '/' + db_info['database'] + \
                            '?driver=ODBC+Driver+17+for+SQL+Server')
        self.database = db_info['database']

    def get_tables(self):
        """Get a list of table in the database"""

        ins = inspect(self.sqlcon)
        return ins.get_table_names()

    def get_columns(self, table):
        """Fetch columns from a table"""
        ins = inspect(self.sqlcon)
        columns_description = ins.get_columns(table)
        return [item['name'] for item in columns_description]

    def get_distinct_items(self, table, column):
        """Get distinct item of a column"""
        with self.sqlcon.connect() as conn:
            query = text("""SELECT DISTINCT %s FROM %s;"""%(column, table))
            result = conn.execute(query)
            data = result.fetchall()
        return [a[0].strip() for a in data]

    def get_filtered_data(self, table, columns, with_date=True, column_to_match=None, value_to_match=None):
        """Get columns data from table where column_to_match = value_to_match"""
        select_columns = ', '.join(columns)
        if with_date:
            if column_to_match is None:
                query = text("""SELECT Date, %s FROM %s.dbo.%s"""%(select_columns, self.database, table))
            else:
                query = text("""SELECT Date, %s FROM %s WHERE %s = '%s' ORDER BY Date ASC;"""%(select_columns, table,
                                                                    column_to_match, value_to_match))
            print(query)
            return pd.read_sql(query, self.sqlcon, index_col='Date', parse_dates='Date')
        else:
            if column_to_match is None:
                query = text("""SELECT %s FROM %s"""%(select_columns, table))
            else:
                query = text("""SELECT %s FROM %s WHERE %s = '%s';"""%(select_columns, table,
                                                                    column_to_match, value_to_match))
            return pd.read_sql(query, self.sqlcon)
    
    def close(self):
        self.sqlcon.dispose()

def sp500_market_breadth_prep():
    from ..market_breadth import sp500Const as spconst
    mb_dir = spconst.sp500_sectorsDir_marketBreadthConst
    mb_df = pd.read_csv(mb_dir+"/20MA.csv", parse_dates=[0])
    sp500 = web.DataReader('^GSPC', 'yahoo', mb_df['Date'].min(), mb_df['Date'].max())#， api_key=QUANDL_KEY)
    sp500.reset_index(inplace=True)