# -*- coding: utf-8 -*-
"""
@author: haoli
"""
import sys
sys.path.append("../")

import pandas as pd
from datetime import datetime
import pyodbc
import numpy as np

import win32com.client
import os
import ntpath
from urllib.request import urlopen, Request
import requests

from pathlib import Path


import key as pconst
_server = pconst.RYAN_SQL['server']
_username = pconst.RYAN_SQL['username']
_password = pconst.RYAN_SQL['password']  
_database = 'SP500_Ratios'    

pd.set_option('mode.chained_assignment', None)

# url_Wilshire5000GDP = 'https://www.gurufocus.com/economic_indicators/60/ratio-of-wilshire-5000-over-gnp'

# #---3 month -- 
# url_salePerShare = 'https://www.gurufocus.com/economic_indicators/101/sp-500-sales-per-share'

_sqlTable_SP500_SP500_OperatingEPS_EstimateTTM = 'SP500_OperatingEPS_EstimateTTM'


def sql_guru_OperatingEPS_estimate(df, dbName):
    df = df.replace({np.NAN: None})
    df[df.columns[1]] = df[df.columns[1]].str.slice(0,35) 
    
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server+';DATABASE='+_database+';UID='+_username+';PWD='+_password)
    cursor = cnxn.cursor()
    
    for index, row in df.iterrows():
        dateStr = row[0]     
        query = """DELETE FROM %s where Date = '%s' and [Sector] = '%s' ;""" % (dbName, dateStr, row[1])
        cursor.execute(query) 
        params = tuple(row)
        query = """INSERT INTO %s VALUES (?,?,?,? );""" %(dbName)
        cursor.execute(query, params)        
    cnxn.commit()        
    cursor.close()
    cnxn.close() 
def extract_allExcelFileSubFolders_toSql():
    # pathlist = Path(sourceDir).glob('**/*.*')
    # pathlist = Path(sourceDir).glob('**/*.xlsx')
    dbName = _sqlTable_SP500_SP500_OperatingEPS_EstimateTTM
    sourceDir = './OperatingEPS'
    pathlist = Path(sourceDir).glob('**/*.xlsx')
    for path in pathlist:
         # because path is object not string
         excelFileFullPath = str(path)
         df = pd.read_excel(excelFileFullPath)
         sql_guru_OperatingEPS_estimate(df, dbName)
# extract_allExcelFileSubFolders_toSql()

#-------------------------------------

def sp500_OperatingEPS_estimate_TTM(url, sectorName):    
    header = {
      "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
      "X-Requested-With": "XMLHttpRequest"
    }    
    r = requests.get(url, headers=header)    
    tables = pd.read_html(r.text)
    df = tables[0]
    df[df.columns[2]] = df[df.columns[2]].str.replace("%","")
    df.insert(1, 'Sector', sectorName)
    print("sp500_OperatingEPS_estimate TTM:  " + sectorName)
    return df

def sp500_OperatingEPS_estimate_monthly_Q():   
    dbName = _sqlTable_SP500_SP500_OperatingEPS_EstimateTTM
    
    url_Total = 'https://www.gurufocus.com/economic_indicators/4202/sp-500-operating-eps-with-estimate-ttm'
    sectorName_Total = "Total"
    df_Total = sp500_OperatingEPS_estimate_TTM(url_Total, sectorName_Total)
    sql_guru_OperatingEPS_estimate(df_Total, dbName)     

    url_CommunicationServices = 'https://www.gurufocus.com/economic_indicators/4210/sp-500-operating-eps-communication-services-ttm'
    sectorName = "CommunicationServices"
    df = sp500_OperatingEPS_estimate_TTM(url_CommunicationServices, sectorName)
    sql_guru_OperatingEPS_estimate(df, dbName) 
    
    url_Energy = 'https://www.gurufocus.com/economic_indicators/4211/sp-500-operating-eps-energy-ttm'
    sectorName = "Energy"
    df = sp500_OperatingEPS_estimate_TTM(url_Energy, sectorName)
    sql_guru_OperatingEPS_estimate(df, dbName)    
    
    url_Industrials  = 'https://www.gurufocus.com/economic_indicators/4212/sp-500-operating-eps-industrials-ttm'
    sectorName = "Industrials"
    df = sp500_OperatingEPS_estimate_TTM(url_Industrials, sectorName)
    sql_guru_OperatingEPS_estimate(df, dbName) 
    
    url_InformationTechnology = 'https://www.gurufocus.com/economic_indicators/4213/sp-500-operating-eps-information-technology-ttm'
    sectorName = "InformationTechnology"
    df = sp500_OperatingEPS_estimate_TTM(url_InformationTechnology, sectorName)
    sql_guru_OperatingEPS_estimate(df, dbName) 
    
    url_Utilities = 'https://www.gurufocus.com/economic_indicators/4209/sp-500-operating-eps-utilities-ttm'
    sectorName = "Utilities"
    df = sp500_OperatingEPS_estimate_TTM(url_Utilities, sectorName)
    sql_guru_OperatingEPS_estimate(df, dbName)    
    
    url_HealthCare = 'https://www.gurufocus.com/economic_indicators/4208/sp-500-operating-eps-health-care-ttm'
    sectorName = "HealthCare"
    df = sp500_OperatingEPS_estimate_TTM(url_HealthCare, sectorName)
    sql_guru_OperatingEPS_estimate(df, dbName) 
    
    url_Materials  = 'https://www.gurufocus.com/economic_indicators/4203/sp-500-operating-eps-materials-ttm'
    sectorName = "Materials"
    df = sp500_OperatingEPS_estimate_TTM(url_Materials, sectorName)
    sql_guru_OperatingEPS_estimate(df, dbName)  
    
    url_ConsumerDiscretionary = 'https://www.gurufocus.com/economic_indicators/4204/sp-500-operating-eps-consumer-discretionary-ttm'
    sectorName = "ConsumerDiscretionary"
    df = sp500_OperatingEPS_estimate_TTM(url_ConsumerDiscretionary, sectorName)
    sql_guru_OperatingEPS_estimate(df, dbName) 
    
    url_RealEstate = 'https://www.gurufocus.com/economic_indicators/4206/sp-500-operating-eps-real-estate-ttm'
    sectorName = "RealEstate"
    df = sp500_OperatingEPS_estimate_TTM(url_RealEstate, sectorName)
    sql_guru_OperatingEPS_estimate(df, dbName)  
    
    url_ConsumerStaples = 'https://www.gurufocus.com/economic_indicators/4207/sp-500-operating-eps-consumer-staples-ttm'
    sectorName = "ConsumerStaples"
    df = sp500_OperatingEPS_estimate_TTM(url_ConsumerStaples, sectorName)
    sql_guru_OperatingEPS_estimate(df, dbName)        
    
    url_Financials = 'https://www.gurufocus.com/economic_indicators/4205/sp-500-operating-eps-financials-ttm'
    sectorName = "Financials"
    df = sp500_OperatingEPS_estimate_TTM(url_Financials, sectorName)
    sql_guru_OperatingEPS_estimate(df, dbName)     
    
sp500_OperatingEPS_estimate_monthly_Q()

