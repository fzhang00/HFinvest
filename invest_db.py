"""
A set of functions and classes to store and read data from our investment database
"""


import pyodbc
import pandas as pd
import numpy as np
# import sp500Const as const
import sqlalchemy
from sqlalchemy import text, inspect
from personal import QUANDL_KEY, RYAN_SQL, FAN_SQL
import pandas_datareader as web
import datetime




#cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password)
# sqlcon = sqlalchemy.create_engine('mssql+pyodbc://'+database_fan['username']+':'+database_fan['password']+\
#                                   '@' + database_fan['server'] + \
#                                   '/' + database_fan['database'] + \
#                                   '?driver=ODBC+Driver+17+for+SQL+Server')

# 
# load source csv
# df = pd.read_csv(const.sp500Info_file_const, index_col=0,
                #  parse_dates = ['Date first added'])
# df = df.replace(np.nan, None, regex=True)
# df = df.sort_index()
# df.to_sql('SP500_COMPANY_INFO', sqlcon, if_exists='replace')
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

def data_to_sql(symbol_list, data_source, 
                engine, db, table_name,
                start_date, end_date,
                if_exists='append', api_key=None):
    """Given a list of symbols, and data source, fetch data and save to SQL database.
    from start_date and end_date.

    Dependency: pandas_datareader

    Input:
        symbol_list: a list of symbol from your data source
        data_source: data source name supported by pandas_datareader
        api_key: api_key for data_source
        conn: sqlalchemy connection engine
        table_name: Table that data would be stored
        start_date, end_date: datetime.datetime object
        if_exists: 'fail', 'replace', or 'append'. Default setting is 'append'.
        """

    # If append, connect to database and fetch the lastest row of data to get last recorded date.
    # Delete the last date record, as it will be re-written. 
    if if_exists == 'append':
        with engine.connect() as conn:
            query = """SELECT TOP (1) * FROM %s.dbo.%s ORDER BY [Date] DESC;"""%(db,table_name)
            last_data = pd.read_sql(query, conn, index_col='Date', parse_dates='Date')
            query = text("DELETE FROM %s.dbo.%s WHERE [Date] = '%s.000'"%(db, table_name, last_data.index[-1]))
            conn.execute(query)
        new_data = web.DataReader(symbol_list, data_source,
                                last_data.index[-1], end_date, api_key=api_key)
    else: # Not appending, simply do as user asks. 
        new_data = web.DataReader(symbol_list, data_source,
                                start_date, end_date, api_key=api_key)
    new_data.to_sql(table_name, engine, if_exists=if_exists, index_label='Date')



def csv_to_sql(file_name, engine, table_name, if_exists):
    """use pd.to_sql to store a csv file into sql. 

    Input:
        file_name: csv file name
        engine: sqlalchemy connection engine
        table_name: sql table name
        if_exists: "append" or "replace"
    """
    data = pd.read_csv(file_name)
    # TODO remove white space. 
    for c in data.columns:
        data[c.strip()] = data[c].str.strip() # remove white space in column name
    data.to_sql(table_name, engine, if_exists=if_exists, index=False)
