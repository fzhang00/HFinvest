import sys
sys.path.append("../")
import datetime
from sqlalchemy import text, inspect

from invest_db import data_to_sql, InvestDB, csv_to_sql
import personal as pconst

_DEFAULT_START_DATE = datetime.datetime(1970,1,1)
_DEFAULT_END_DATE = datetime.datetime.today()

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
    _FED_SYMBOL_TABLE = "FED_US_SYMBOL"
    _FED_TABLE_PREFIX = "FED_"

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

db_info = pconst.RYAN_SQL
db_info['database'] = "FED"
update_fred_data(db_info)
