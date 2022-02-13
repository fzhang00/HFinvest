import sys
sys.path.append("..\\")
sys.path.append("..\\..\\InvestPlots\\invest")
import datetime
from sqlalchemy import text, inspect

import pandas as pd
from invest_db import InvestDB
import key as pconst

_DEFAULT_START_DATE = datetime.datetime(1970,1,1)
_DEFAULT_END_DATE = datetime.datetime.today()
_FED_SYMBOL_TABLE = "FED_US_SYMBOL"
_FED_TABLE_PREFIX = "FED_"

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
    # Excel sometimes fill white space when extract to csv
    # remove white space in column name. 
    data.rename(columns = {c:c.strip() for c in data.columns}, inplace=True)
    # remove white space in data
    for c in data.columns:
        data[c] = data[c].str.strip()
    data.to_sql(table_name, engine, if_exists=if_exists, index=False)

def fred_to_sql(symbol_list, db, table_name, start_date=_DEFAULT_START_DATE,
                end_date=_DEFAULT_END_DATE):
    """Given a list of symbols,  
    Download data using data reader and store them in database. """
    ins = inspect(db.sqlcon)
    db_tables = ins.get_table_names()
    if table_name in db_tables:
        data_to_sql(symbol_list, 'fred', db.sqlcon, db.database,
                    table_name, start_date = _DEFAULT_START_DATE,
                    end_date = _DEFAULT_END_DATE, if_exists='append')
    else: #no such DB name, new list? create
        data_to_sql(symbol_list, 'fred', db.sqlcon, db.database,
                    table_name, start_date = _DEFAULT_START_DATE,
                    end_date = _DEFAULT_END_DATE, if_exists='replace')


def update_fred_data(db_info):
    """Update FED data using symbol included in FED_US_SYMBOL table
    """
    db = InvestDB(db_info)
    ins = inspect(db.sqlcon)
    db_tables = ins.get_table_names()
    if _FED_SYMBOL_TABLE not in db_tables:
        # Symbol table not in db table list, add it in.
        # This symbol list is compiled manually from FRED spreadsheet add-in
        csv_to_sql("FRED_symbol.csv", db.sqlcon, _FED_SYMBOL_TABLE, "replace")
    # Grab data on Symbol List
    # select distinc category, one category per table
    categories = db.get_distinct_items(_FED_SYMBOL_TABLE, 'Category')
    for c in categories:
        # get symbol list for category c
        symbol_lst = db.get_filtered_data(_FED_SYMBOL_TABLE, ['Symbol'],
                                        with_date=False, 
                                        column_to_match='Category',
                                        value_to_match=c)
        table_name = _FED_TABLE_PREFIX+'_'.join((c.upper()).split(' '))
        print("Working on table", table_name)
        # Fetch data from FRED and populate sql table. Table will be created if not exists.
        fred_to_sql(symbol_lst['Symbol'], db, table_name)
    db.close()

def update_fred_symbol_table( db_info, symbol_file="FRED_symbol.csv"):
    db = InvestDB(db_info)
    data = pd.read_csv(symbol_file)
    data.rename(columns = {c:c.strip() for c in data.columns}, inplace=True)
    for c in data.columns:
        data[c] = data[c].str.strip()
    data.to_sql(_FED_SYMBOL_TABLE, db.sqlcon, if_exists="replace", index=False)
    db.close()

db_info = pconst.RYAN_SQL
db_info['database'] = "FED"
#update_fred_data(db_info)
update_fred_symbol_table(db_info, "FRED_symbol.csv")