# -*- coding: utf-8 -*-
"""
@author: haoli
"""
import sys
sys.path.append("../")

import pandas as pd
# from datetime import datetime
import pyodbc
import numpy as np

# import win32com.client
# import os
# import ntpath
from urllib.request import urlopen, Request
import requests

from pathlib import Path


import key as pconst
_server = pconst.RYAN_SQL['server']
_username = pconst.RYAN_SQL['username']
_password = pconst.RYAN_SQL['password']  
_database = 'SP500_Ratios'     


pd.set_option('mode.chained_assignment', None)


# url_PE_shiller_multpl = 'https://www.multpl.com/shiller-pe/table/by-month'
# url_Wilshire5000GDP = 'https://www.gurufocus.com/economic_indicators/60/ratio-of-wilshire-5000-over-gnp'


_sqlTable_SP500_ClosePrice_PerSales = 'SP500_ClosePrice_PerSales'


def sql_guru_SP500_ClosePrice_PerSales(df, dbName):
    df = df.replace({np.NAN: None})
    # df[df.columns[1]] = df[df.columns[1]].str.slice(0,35) 
    
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server+';DATABASE='+_database+';UID='+_username+';PWD='+_password)
    cursor = cnxn.cursor()
    
    for index, row in df.iterrows():
        dateStr = row[0]     
        query = """DELETE FROM %s where Date = '%s' ;""" % (dbName, dateStr)
        cursor.execute(query) 
        params = tuple(row)
        query = """INSERT INTO %s VALUES (?,?,? );""" %(dbName)
        cursor.execute(query, params)        
    cnxn.commit()        
    cursor.close()
    cnxn.close() 
def extract_allExcelFileSubFolders_toSql():
    # pathlist = Path(sourceDir).glob('**/*.*')
    # pathlist = Path(sourceDir).glob('**/*.xlsx')
    dbName = _sqlTable_SP500_ClosePrice_PerSales
    sourceDir = './PricePerSales'
    pathlist = Path(sourceDir).glob('**/*.xlsx')
    for path in pathlist:
         # because path is object not string
         excelFileFullPath = str(path)
         df = pd.read_excel(excelFileFullPath)
         sql_guru_SP500_ClosePrice_PerSales(df, dbName)
# extract_allExcelFileSubFolders_toSql()
# print()
#-------------------------------------

def sp500_SalesPerShare_estimate(url):    
    header = {
      "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
      "X-Requested-With": "XMLHttpRequest"
    }    
    r = requests.get(url, headers=header)    
    tables = pd.read_html(r.text)
    df = tables[0]
    df[df.columns[2]] = df[df.columns[2]].str.replace("%","")
    # df.insert(1, 'Sector', sectorName)
    print("sp500 close price per sales: download ")
    return df


def SP500_ClosePrice_PerSales_daily_Q():   
    dbName = _sqlTable_SP500_ClosePrice_PerSales
    
    url_Total = 'https://www.gurufocus.com/economic_indicators/4238/sp-500-price-to-sales'
    # sectorName_Total = "Total"
    df_Total = sp500_SalesPerShare_estimate(url_Total)
    sql_guru_SP500_ClosePrice_PerSales(df_Total, dbName)       
   
    
SP500_ClosePrice_PerSales_daily_Q()

