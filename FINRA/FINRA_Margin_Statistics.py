# -*- coding: utf-8 -*-
"""
Created on Wed May 12 21:35:04 2021

@author: haoli
"""
import sys
sys.path.append("../")

import pandas as pd
from datetime import datetime
import pyodbc
import numpy as np


import FINRA.Const_FINRA as myFINRA

import key as pconst
_server = pconst.RYAN_SQL['server']
_username = pconst.RYAN_SQL['username']
_password = pconst.RYAN_SQL['password']  
_database = 'FINRA' 
      

_sqlTable_FINRA_monthly_Margin_Stast= 'FINRA_monthly_Margin_Stast'

pd.set_option('mode.chained_assignment', None)

#--------------------

def getDateFromString(dateStr): 

    d = dateStr.strip()
    try: # DD-MM-YYYY        
        date_fromFile = datetime.strptime(d, "%b-%y")
    except ValueError:
        # try another format
        try:
            date_fromFile = datetime.strptime(d, "%B-%y") 
            # d.strftime("%A %d. %B %Y")
            # 'Monday 11. March 2002'
        except ValueError:
            try:
                date_fromFile = datetime.strptime(d, '%d %b %Y') # LME gold 01 Apr
                # print (datetime.strptime(date_str, "%m-%d"))
            except ValueError:
                try:
                    # date_fromFile = datetime.strptime(d, '%Y年%m月%d日')  
                    date_fromFile = datetime.strptime(d, '%b.%d,%Y')  #Date:Mar.05,2021
                except ValueError:                
                    print('9999')
                    print (d)
                    return d
    return date_fromFile
    # return date_fromFile.strftime('%Y-%m-%d')

def convertDDMM_date(df):
    for i in range(len(df)): 
        dateStr = df.iloc[i][0]
        dateStr = dateStr.replace('Sept', 'Sep')        
        dateObj = getDateFromString(dateStr)
        df.iat[i, 0] = dateObj
    return df

def sql_monthly_marginStast(df, dbName):
    df = df.replace({np.NAN: None})
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server+';DATABASE='+_database+';UID='+_username+';PWD='+_password)
    cursor = cnxn.cursor()
    
    for index, row in df.iterrows():
        dateStr = row[0]     
        query = """DELETE FROM %s where Date = '%s' ;""" % (dbName, dateStr)
        cursor.execute(query)         

        params = tuple(row)
        query = """INSERT INTO %s VALUES (?,?,?,? );""" %(dbName)
        cursor.execute(query, params)        
    cnxn.commit()        
    cursor.close()
    cnxn.close() 
    

def sql_excelFile_Margin_Statistics(fileFullPath, dbName):
    df = pd.read_excel(fileFullPath)   
    colDate = 'Year-Month'	
    # colDebit = "Debit Balances in Customers' Securities Margin Accounts"
    # colCreditCash =	"Free Credit Balances in Customers' Cash Accounts"	
    # colCreditMargin =    "Free Credit Balances in Customers' Securities Margin Accounts"    
    df[colDate] = pd.to_datetime(df[colDate], format = '%Y-%m') 
    for col in  df.columns[1:]:
        df[col] = pd.to_numeric(df[col], errors='coerce',downcast= 'integer')        
    sql_monthly_marginStast(df, dbName)
    
# fileFullPath =  myFINRA.FINRA_Dir_MarginStatistics + '/2021-04_margin-statistics.xlsx'
# dbName = _sqlTable_FINRA_monthly_Margin_Stast   
# sql_excelFile_Margin_Statistics(fileFullPath, dbName)  
# print()  

def html_monthly_3ndWeek_Margin_Statistics():    
    url = myFINRA._FINRA_MarginStatistics_URL
    # url = 'https://www.finra.org/investors/learn-to-invest/advanced-investing/margin-statistics'
    tb = pd.read_html(url)    
    df = tb[0].dropna(how='all')
    # colDate = 'Year-Month'  
    # df[colDate] = pd.to_datetime(df[colDate], format = '%Y-%m')     
    convertDDMM_date(df)
    for col in  df.columns[1:]:
        df[col] = pd.to_numeric(df[col], errors='coerce',downcast= 'integer')
        
    dbName = _sqlTable_FINRA_monthly_Margin_Stast     
    sql_monthly_marginStast(df, dbName)       
    # df = tb[0]
    # df = convertDDMM_date(df)
    # for i in range(len(tb) -1 ):
    #     df1 = tb[i+1].dropna(how='all')
    #     df1 = convertDDMM_date(df1)        
    #     df = df.append(df1, ignore_index = True)

# html_monthly_3ndWeek_Margin_Statistics()  


#----------OVER THE COUNTER--------------------------

# import requests
# def html_monthly_OTC_Equities():    
#     url = './MarginStatistics/Market Statistics - Equity Trading Data Monthly.html'
#     # url = 'https://otce.finra.org/otce/marketStatistics'
    
#     # header = {
#     #   "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
#     #   "X-Requested-With": "XMLHttpRequest"
#     # }
    
#     # r = requests.get(url, headers=header)
    
#     # dfs = pd.read_html(r.text)    
#     # print(dfs)
    
#     tb = pd.read_html(url)    
#     df1 = tb[0].dropna(how='all')
#     df = df1.iloc[:, 1:-1]
#     # colDate = 'Year-Month'  
#     # df[colDate] = pd.to_datetime(df[colDate], format = '%Y-%m')     
#     convertDDMM_date(df)
#     for col in  df.columns[2:]:
#         df[col] = pd.to_numeric(df[col], errors='coerce',downcast= 'integer')
        
#     dbName = _sqlTable_FINRA_monthly_Margin_Stast     
#     sql_monthly_marginStast(df, dbName)
# html_monthly_OTC_Equities()

  
						
