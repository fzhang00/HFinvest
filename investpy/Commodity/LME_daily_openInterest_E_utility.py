# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 13:15:30 2021

@author: haoli

"""

import sys
sys.path.append("../")

import const_common as constA
# import downloadUpdateData as mydownPy
import Const_LME_A as constLME_a


# import requests
from os import makedirs
import os.path as myPath
# import os

import pandas as pd

# from urllib.request import urlopen, Request

# import pyautogui, time
#Set up a 2.5 second pause after each PyAutoGUI call:
# pyautogui.PAUSE = 2.5

# from selenium import webdriver
from datetime import datetime
# import ntpath

from pathlib import Path

import pyodbc
import numpy as np

# from urllib.request import urlopen, Request


#----------------------------------
errorFileTargetDir = '../'

_dateSearchBy_ClassName_nonFerrous_gold_silver = "delayed-date.left"
_dateSearchKeyword = "Data valid for"
_waitTime_loadWebsite_LME = 3

_columnName_goldSilver = ['Date', 'Volume', 'Open Interest']

_server = 'RyanPC'
_database = 'Commodity_A1' 
_username = 'hl' 
_password = '123'     

_sqlTable_LME_baseMetal_stock = 'LME_baseMetal_stock'
_sqlTable_LME_baseMetal_price = 'LME_baseMetal_price'
_sqlTable_LME_precious_price = 'LME_precious_price'
_sqlTable_LME_precious_VolOpenInterest = 'LME_precious_VolOpenInterest'

_sqlTable_LME_TraderReport_CA = 'LME_weeklyTraderReport_CA'
_sqlTable_LME_TraderReport_AL = 'LME_weeklyTraderReport_AL'
_sqlTable_LME_TraderReport_gold = 'LME_weeklyTraderReport_Gold'
_sqlTable_LME_TraderReport_silver = 'LME_weeklyTraderReport_Silver'

_sqlTable_LME_daily_Volume = 'LME_Daily_Volume'

_sqlTable_LME_daily_OpenInterest_option = 'LME_Daily_OpenInterest_Option_E'
_sqlTable_LME_daily_OpenInterest_future = 'LME_Daily_OpenInterest_Future_E'


_REPORT_DATE_col    = 'REPORT_DATE'
_FORWARD_DATE_col   = 'FORWARD_DATE'
_FORWARD_MONTH_col  = 'FORWARD_MONTH'

# mydownPy.logError("my test message")
#logError(errorFileTargetDir, msg)
# mydownPy.logError(errorFileTargetDir, "my test message")


#------- ---------

def makeTodayDataDir(newDir):
    # if not myPath.lexists(newDir): #lexists
    if not myPath.exists(newDir):
        makedirs(newDir)

def convertDDMM_date(df):
    for i in range(len(df)): 
        d = df.iloc[i][0]        
        d2 = d.strip()
        yy = datetime.strptime(d2, '%Y%m%d').strftime('%Y-%m-%d')
        df.iat[i, 0] = yy
    return df  

#--------------------------------
def sql_openInterest_daily_Option(df, dbName): 
    # --- SQL ----
    df = df.replace({np.NAN: None})
    df[df.columns[2]] = df[df.columns[2]].str.slice(0,17)
    
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server+';DATABASE='+_database+';UID='+_username+';PWD='+_password)
    cursor = cnxn.cursor()
    
    #delete today data before enter
    dateStr = df.iloc[1,0]
    # productStr = row[1] 
    # descriptionStr  = row[2]       
    query = """DELETE FROM %s where Date = '%s';""" % (dbName, dateStr)
    cursor.execute(query)        
    
    for index, row in df.iterrows():     

        params = tuple(row)
        query = """INSERT INTO %s VALUES (?,?,?,?, ?,?,?,?);""" %(dbName)
        cursor.execute(query, params)        
    cnxn.commit()        
    cursor.close()
    cnxn.close()  
    
def sql_openInterest_daily_Future(df, dbName): 
    df = df.replace({np.NAN: None})
    df[df.columns[2]] = df[df.columns[2]].str.slice(0,17)

    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server+';DATABASE='+_database+';UID='+_username+';PWD='+_password)
    cursor = cnxn.cursor()    
    for index, row in df.iterrows(): 
        #delete today data before enter
        #Date	UNDERLYING	ContractType	ForwardDate	OpenInterest	Turnover
        
        
#--------disable this when load large files------------------------        
        query = """DELETE FROM %s where Date = '%s' and [Underlying] = '%s' and [ContractType] = '%s' and [ForwardDate] ='%s';""" \
                % (dbName, row[0], row[1], row[2],row[3])
        cursor.execute(query)          
#---------------------------------------

        
        params = tuple(row)
        query = """INSERT INTO %s VALUES (?,?,?,?, ?,? );""" %(dbName)
        cursor.execute(query, params)        
    cnxn.commit()        
    cursor.close()
    cnxn.close() 

def extract_OpenInterestData_Preciou_sql(fileFullPath, dbNameFuture):
    # df.astype(str)  # df = pd.read_csv(fileFullPath, dtype=str)   
    df = pd.read_csv(fileFullPath)    
    df1 = df.dropna(how='all')
    df_data = df1.dropna(axis = 1, how='all') 
    # df2 = df1.dropna(axis = 1, how='all') 
    
    #-- convert integer to datatime format
    df_data[_REPORT_DATE_col] = (pd.to_datetime(df_data[_REPORT_DATE_col], format = '%Y%m%d'))
    df_data[_FORWARD_DATE_col] = (pd.to_datetime(df_data[_FORWARD_DATE_col], format = '%Y%m%d')) 
   
    
    #--------aggrate the data   
    df_future = df_data.groupby([_REPORT_DATE_col,'UNDERLYING','CONTRACT_TYPE', 
                                 pd.Grouper(key=_FORWARD_DATE_col,freq='M') ]).agg({'OPEN_INTEREST':sum,'TURNOVER':sum})
    
    df_future1 = df_future.reset_index() 
    #----write the data to csv file.    
    if not df_future1.empty:        
        dateStr = df_future1.iloc[1,0].strftime('%Y-%m-%d')
        filePath = constA.getFilePathInfo(fileFullPath, 0)
        fileName = constA.getFilePathInfo(fileFullPath, 2)
        fileFullPath_new = filePath + '/' + dateStr + '_Future_' + fileName +'.csv'
        df_future1.to_csv(fileFullPath_new, index = False, date_format ='%Y-%m-%d')    
        print ("daily exchange options processed: " + fileFullPath)    
        
        #--------sql--------
        sql_openInterest_daily_Future(df_future1, dbNameFuture) 

# fileFullPath = constLME_a.commodityLME_openInterestDir_precious +'/Exchange Open Interest - precious - 05 May 2021.csv'
# dbNameFuture = _sqlTable_LME_daily_OpenInterest_future
# extract_OpenInterestData_Preciou_sql(fileFullPath, dbNameFuture)
# print()

    
def extract_OpenInterestData_Base_sql(fileFullPath, dbNameOption, dbNameFuture):
    # df.astype(str)  # df = pd.read_csv(fileFullPath, dtype=str)   
    df = pd.read_csv(fileFullPath)    
    df1 = df.dropna(how='all')
    # df_data = df1.dropna(axis = 1, how='all') 
    df2 = df1.dropna(axis = 1, how='all') 
    
    #------rows with AH and CA only
    boolseries = df2[df2.columns[1]].str.contains(r'ca|ah', case = False, na= False)   
    df_data = df2.loc[(boolseries)]
    # if df_data.empty:
    #     df_data = df2

    #-- convert integer to datatime format
    df_data[_REPORT_DATE_col] = (pd.to_datetime(df_data[_REPORT_DATE_col], format = '%Y%m%d'))
    df_data[_FORWARD_DATE_col] = pd.to_datetime(df_data[_FORWARD_DATE_col], format = '%Y%m%d')
    df_data[_FORWARD_MONTH_col] = pd.to_datetime(df_data[_FORWARD_MONTH_col], format = '%Y%m')

    #--------------
    #REPORT_DATE	UNDERLYING	CURRENCY	CONTRACT_TYPE	SUB_CONTRACT_TYPE	
    #FORWARD_DATE	FORWARD_MONTH	STRIKE	OPEN_INTEREST	TURNOVER
    #    pd.Grouper(key=('FORWARD_MONTH'), freq='MS',)  ] )['STRIKE'].mean() 
    #grouped['Points'].agg([np.sum, np.mean, np.std])
     # group.agg({'STRIKE' : 'mean' , 'OPEN_INTEREST': 'sum', 'TURNOVER': 'sum'})
     
     #--------aggrate the data
    df_option = df_data.groupby([_REPORT_DATE_col,'UNDERLYING', 'CONTRACT_TYPE',
                             'SUB_CONTRACT_TYPE', 
                             pd.Grouper(key=(_FORWARD_MONTH_col), freq='M',)  ] ).agg({'STRIKE' : 'mean' , 'OPEN_INTEREST': 'sum', 'TURNOVER': 'sum'})
    
    df_future = df_data.groupby([ _REPORT_DATE_col,'UNDERLYING', 'CONTRACT_TYPE', 
                             pd.Grouper(key=(_FORWARD_DATE_col), freq='M')  ] ).agg({'OPEN_INTEREST': 'sum', 'TURNOVER': 'sum'})

    df_option1 = df_option.reset_index()
    df_future1 = df_future.reset_index()  
    
    #----write the data to csv file.
    if not df_option1.empty:        
        dateStr = df_option1.iloc[1,0].strftime('%Y-%m-%d')
        filePath = constA.getFilePathInfo(fileFullPath, 0)
        fileName = constA.getFilePathInfo(fileFullPath, 2)
        fileFullPath_new = filePath + '/' + dateStr + '_Option_' + fileName +'.csv'
        df_option1.to_csv(fileFullPath_new, index = False, date_format ='%Y-%m-%d', float_format='%.1f' )    
        print ("daily exchange options processed: " + fileFullPath)

        #--------sql--------
        sql_openInterest_daily_Option(df_option1, dbNameOption)
    
    if not df_future1.empty:        
        dateStr = df_future1.iloc[1,0].strftime('%Y-%m-%d')
        filePath = constA.getFilePathInfo(fileFullPath, 0)
        fileName = constA.getFilePathInfo(fileFullPath, 2)
        fileFullPath_new = filePath + '/' + dateStr + '_Future_' + fileName +'.csv'
        df_future1.to_csv(fileFullPath_new, index = False, date_format ='%Y-%m-%d')    
        print ("daily exchange options processed: " + fileFullPath)    
        
        #--------sql--------
        sql_openInterest_daily_Future(df_future1, dbNameFuture)
    
    # #df['just_date'] = df['dates'].dt.date
    # for group_name, df_group in group:
    #     print (group_name) 
    #     print (df_group)
    #     print()    

# fileFullPath = constLME_a.commodityLME_openInterestDir_base +'/Exchange Open Interest - base - 06 May 2021.csv'
# dbNameOption = _sqlTable_LME_daily_OpenInterest_option
# dbNameFuture = _sqlTable_LME_daily_OpenInterest_future
# extract_OpenInterestData_Base_sql(fileFullPath, dbNameOption, dbNameFuture)
# print()


#---------------------------------------
def extract_all_Base_csvFileSubFolders_toSql(sourceDir, dbNameOption, dbNameFuture):
    # pathlist = Path(sourceDir).glob('**/*.*')
    # pathlist = Path(sourceDir).glob('**/*.xlsx')
    pathlist = Path(sourceDir).glob('**/*.csv')
    for path in pathlist:
         # because path is object not string
         csvFullPath = str(path)
         fileFullPath = csvFullPath         
         extract_OpenInterestData_Base_sql(fileFullPath, dbNameOption, dbNameFuture)
         
# sourceDir = constLME_a.commodityLME_openInterestDir_base + '/dailyHistoryFile'
# sourceDir = constLME_a.commodityLME_openInterestDir_base + '/workFolder'
# dbNameFuture = _sqlTable_LME_daily_OpenInterest_future         
# dbNameOption = _sqlTable_LME_daily_OpenInterest_option
# extract_all_Base_csvFileSubFolders_toSql(sourceDir, dbNameOption, dbNameFuture)

def extract_all_PreciousFuture_csvFileSubFolders_toSql(sourceDir, dbNameFuture):
    # pathlist = Path(sourceDir).glob('**/*.*')
    # pathlist = Path(sourceDir).glob('**/*.xlsx')
    pathlist = Path(sourceDir).glob('**/*.csv')
    for path in pathlist:
         csvFullPath = str(path)
         fileFullPath = csvFullPath
         extract_OpenInterestData_Preciou_sql(fileFullPath, dbNameFuture)  
         
# sourceDir = constLME_a.commodityLME_openInterestDir_precious + '/dailyHistoryFile'
# sourceDir = constLME_a.commodityLME_openInterestDir_precious + '/workFolder'
# dbNameFuture = _sqlTable_LME_daily_OpenInterest_future  
# extract_all_PreciousFuture_csvFileSubFolders_toSql(sourceDir, dbNameFuture)
# print()


         
def extract_Monthly(fileFullPath, targetDir, fileNameAdd):
    df = pd.read_csv(fileFullPath, dtype=str)    
    df_groups = df.groupby('REPORT_DATE')
    # # iterate over each group
    for group_name, df_group in df_groups:
        # print ('c1: ' + group_name) 
        # print (df_group)
        targetFileFullPath = targetDir + '/' + group_name+ fileNameAdd
        df_group.to_csv(targetFileFullPath, index= False)

# fileFullPath = constLME_a.commodityLME_openInterestDir_base + '/2019-2021 baseE/EOI Monthly Base January 2019.csv' 
# targetDir = constLME_a.commodityLME_openInterestDir_base + '/dailyHistoryFile'
# extract_Monthly(fileFullPath, targetDir)
# print()

def extract_Monthly_loop(sourceDir, targetDir, fileNameAdd):
    # pathlist = Path(sourceDir).glob('**/*.*')
    # pathlist = Path(sourceDir).glob('**/*.xlsx')
    pathlist = Path(sourceDir).glob('**/*.csv')
    for path in pathlist:
         csvFullPath = str(path)         
         # fileFullPath = constLME_a.commodityLME_openInterestDir_base + '/2019-2021 baseE/EOI Monthly Base May 2019.csv' 
         fileFullPath = csvFullPath
         # targetDir = constLME_a.commodityLME_openInterestDir_base + '/dailyHistoryFile'
         # fileNameAdd = '_EOI Monthly Base.csv'
         
         extract_Monthly(fileFullPath, targetDir, fileNameAdd)
         
# sourceDir = constLME_a.commodityLME_openInterestDir_base + '/2019-2021 baseE'
# targetDir = constLME_a.commodityLME_openInterestDir_base + '/dailyHistoryFile'
# fileNameAdd = '_EOI Monthly Base.csv'

# sourceDir = constLME_a.commodityLME_openInterestDir_precious + '/2019-2021 preciousE'
# targetDir = constLME_a.commodityLME_openInterestDir_precious + '/dailyHistoryFile'
# fileNameAdd = '_EOI Monthly precious.csv'

# extract_Monthly_loop(sourceDir, targetDir, fileNameAdd)
# print()









#---------------------------------------------------

