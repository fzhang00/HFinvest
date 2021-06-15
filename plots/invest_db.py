"""
A set of functions and classes to store and read data from our investment database
"""

import datetime
import pyodbc
import pandas as pd
import numpy as np
# import sp500Const as const
import sqlalchemy
from sqlalchemy import text, inspect
# from ..key import QUANDL_KEY, RYAN_SQL, FAN_SQL
import pandas_datareader as web
from pltutil import *

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

def get_fed_db_data(db, symbols, 
                    start_date=datetime.datetime(2000,1,1), 
                    end_date=datetime.datetime.today()):
    """Returns a dataframe of FRED data extracted from FED database"""
    symbol_df = db.get_filtered_data('FED_US_SYMBOL', 
                                    ['Symbol', 'Description', 'Category'], 
                                    with_date=False)
    symbol_tb = symbol_df.loc[symbol_df['Symbol'].isin(symbols)]
    symbol_to_download = pd.DataFrame([{'Symbol':s, 'Description':None, 'Category':None }\
                                         for s in symbols if s not in list(symbol_df['Symbol'])])
    print(",".join(list(symbol_to_download['Symbol'])), "is not in database")
    # get distinct Category to construct table
    unique_category = symbol_tb['Category'].unique()
    dfs = []
    changes = {}
    for c in unique_category:
        table_name = 'FED_'+'_'.join(c.upper().split(' '))
        dfs.append(db.get_filtered_data(table_name, 
                                        list(symbol_tb['Symbol'].loc[symbol_tb['Category']==c])
                                        ))
    try:
        dfs.append(web.DataReader(symbol_to_download['Symbol'],'fred', start_date, end_date))
        symbol_tb = pd.concat([symbol_tb, symbol_to_download])
    except web._utils.RemoteDataError:
        print("One of your symbol {} not exists on FRED server.".format(list(symbol_to_download['Symbol'])))
    output=pd.concat(dfs, axis=1)
    for cl in output.columns:
        changes[cl] = compute_change_percentage(output, cl)
    output.reset_index(inplace=True)
    output.rename(columns={'index':'Date'}, inplace=True)
    return output, changes, symbol_tb

def get_sp500_index(start_date=datetime.datetime(2000,1,1), 
                    end_date=datetime.datetime.today()):
    """Returns a dataframe with SP500 INDEX"""
    return web.DataReader('^GSPC', 'yahoo', start_date, end_date)
    

def test():
    db = InvestDB(FAN_SQL)    
    employ_symbols = ['ICSA', 'CCSA', 'JTSJOL', 'JTSHIL','JTSTSL', 'JTSQUL', 'JTSLDL']
    employ_df, employ_changes, symbol_tb= get_fed_db_data(db, employ_symbols)
    print(employ_df.head(3))
    print(employ_changes)
    print(symbol_tb)

if __name__=="__main__":
    test()