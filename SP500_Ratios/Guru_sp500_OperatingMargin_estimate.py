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


# url_PE_shiller_multpl = 'https://www.multpl.com/shiller-pe/table/by-month'
# url_Wilshire5000GDP = 'https://www.gurufocus.com/economic_indicators/60/ratio-of-wilshire-5000-over-gnp'
# #---3 month -- 
# url_salePerShare = 'https://www.gurufocus.com/economic_indicators/101/sp-500-sales-per-share'


_sqlTable_SP500_OperatingMargin_Estimate = 'SP500_OperatingMargin_Estimate'


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
    dbName = _sqlTable_SP500_OperatingMargin_Estimate
    sourceDir = './OperatingMargin'
    pathlist = Path(sourceDir).glob('**/*.xlsx')
    for path in pathlist:
         # because path is object not string
         excelFileFullPath = str(path)
         df = pd.read_excel(excelFileFullPath)
         sql_guru_OperatingEPS_estimate(df, dbName)
# extract_allExcelFileSubFolders_toSql()
# print()
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
    print("sp500_Operating margin estimate:  " + sectorName)
    return df


def sp500_OperatingMargin_estimate_monthly_Q():   
    dbName = _sqlTable_SP500_OperatingMargin_Estimate
    
    url_Total = 'https://www.gurufocus.com/economic_indicators/4226/sp-500-operating-margin'
    sectorName_Total = "Total"
    df_Total = sp500_OperatingEPS_estimate_TTM(url_Total, sectorName_Total)
    sql_guru_OperatingEPS_estimate(df_Total, dbName)     

    url_CommunicationServices = 'https://www.gurufocus.com/economic_indicators/4234/sp-500-operating-margin-communication-services'
    sectorName = "CommunicationServices"
    df = sp500_OperatingEPS_estimate_TTM(url_CommunicationServices, sectorName)
    sql_guru_OperatingEPS_estimate(df, dbName) 
    
    url_Energy = 'https://www.gurufocus.com/economic_indicators/4235/sp-500-operating-margin-energy'
    sectorName = "Energy"
    df = sp500_OperatingEPS_estimate_TTM(url_Energy, sectorName)
    sql_guru_OperatingEPS_estimate(df, dbName)    
    
    url_Industrials  = 'https://www.gurufocus.com/economic_indicators/4236/sp-500-operating-margin-industrials'
    sectorName = "Industrials"
    df = sp500_OperatingEPS_estimate_TTM(url_Industrials, sectorName)
    sql_guru_OperatingEPS_estimate(df, dbName) 
    
    url_InformationTechnology = 'https://www.gurufocus.com/economic_indicators/4237/sp-500-operating-margin-information-technology'
    sectorName = "InformationTechnology"
    df = sp500_OperatingEPS_estimate_TTM(url_InformationTechnology, sectorName)
    sql_guru_OperatingEPS_estimate(df, dbName) 
    
    url_Utilities = 'https://www.gurufocus.com/economic_indicators/4233/sp-500-operating-margin-utilities'
    sectorName = "Utilities"
    df = sp500_OperatingEPS_estimate_TTM(url_Utilities, sectorName)
    sql_guru_OperatingEPS_estimate(df, dbName)    
    
    url_HealthCare = 'https://www.gurufocus.com/economic_indicators/4232/sp-500-operating-margin-health-care'
    sectorName = "HealthCare"
    df = sp500_OperatingEPS_estimate_TTM(url_HealthCare, sectorName)
    sql_guru_OperatingEPS_estimate(df, dbName) 
    
    url_Materials  = 'https://www.gurufocus.com/economic_indicators/4227/sp-500-operating-margin-materials'
    sectorName = "Materials"
    df = sp500_OperatingEPS_estimate_TTM(url_Materials, sectorName)
    sql_guru_OperatingEPS_estimate(df, dbName)  
    
    url_ConsumerDiscretionary = 'https://www.gurufocus.com/economic_indicators/4228/sp-500-operating-margin-consumer-discretionary'
    sectorName = "ConsumerDiscretionary"
    df = sp500_OperatingEPS_estimate_TTM(url_ConsumerDiscretionary, sectorName)
    sql_guru_OperatingEPS_estimate(df, dbName) 
    
    url_Financials = 'https://www.gurufocus.com/economic_indicators/4229/sp-500-operating-margin-financials'
    sectorName = "Financials"
    df = sp500_OperatingEPS_estimate_TTM(url_Financials, sectorName)
    sql_guru_OperatingEPS_estimate(df, dbName)  
    
    url_RealEstate = 'https://www.gurufocus.com/economic_indicators/4230/sp-500-operating-margin-real-estate'
    sectorName = "RealEstate"
    df = sp500_OperatingEPS_estimate_TTM(url_RealEstate, sectorName)
    sql_guru_OperatingEPS_estimate(df, dbName)  
    
    url_ConsumerStaples = 'https://www.gurufocus.com/economic_indicators/4231/sp-500-operating-margin-consumer-staples'
    sectorName = "ConsumerStaples"
    df = sp500_OperatingEPS_estimate_TTM(url_ConsumerStaples, sectorName)
    sql_guru_OperatingEPS_estimate(df, dbName)        
    
   
    
sp500_OperatingMargin_estimate_monthly_Q()

