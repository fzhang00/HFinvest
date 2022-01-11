# -*- coding: utf-8 -*-
"""
@author: haoli
"""
import sys
sys.path.append("../")
import const_common as constA
# import downloadUpdateData as mydownPy

import downloadUpdateData as mydownPy

from datetime import datetime, timedelta
# from datetime import timedelta
# import requests
from os import makedirs

import os.path as myPath
import pandas as pd

# from urllib.request import urlopen, Request
# from pathlib import Path 
import os

import pyodbc
# import numpy as np

import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import ntpath

import pyautogui #, time
pyautogui.PAUSE =2.5

from pathlib import Path


import requests
from bs4 import BeautifulSoup
import re

#----------------------------------
errorFileTargetDir = '../'
# mydownPy.logError("my test message")
#logError(errorFileTargetDir, msg)
# mydownPy.logError(errorFileTargetDir, "my test message")

_dir_Option_CbeoOnly_history = './OptionCbeoOnly_history_VolOI/'
_fileName_sum = 'optionOnly_history_Sum.csv'
_fileName_oex = 'optionOnly_history_OEX.csv'
_oexKey = '(oex)'   #"S&P 100 INDEX - (OEX)"  # 2003
                     # "S AND P 100 INDEX - (OEX)" 2019   (oex)
_fileName_vix = 'optionOnly_history_VIX.csv'
_vixKey = 'cboe volatility index options'            

_fileName_rut = 'optionOnly_history_RUT.csv'
_rutKey = 'russell 2000 index' 
# _rutKey = '(rut)' 

_fileName_SPX = 'optionOnly_history_SPX.csv'
_fileName_SPXW = 'optionOnly_history_SPW.csv'
_noKey = ''

#2003  S AND P 500 INDEX - (SPX)  2003
#2010  S AND P 500 INDEX - (SPX)  --- S AND P 500 INDEX WEEKLYS (NOTE: NO WEEKLYS ARE LISTED THE 2ND FRIDAY OF A MONTH)
#2016 S&P 500 INDEX - (SPX)  S&P 500 INDEX WEEKLYS --- S&P 500 INDEX - PM SETTLED - (SPXPM) ? small   2016
#2019  S&P 500 INDEX (SPX) -----  S&P 500 INDEX - PM SETTLED (SPXW)  2019


_fileName_index = 'optionOnly_history_Index.csv' #only volume
_fileName_equity = 'optionOnly_history_Equity.csv'  #only volume
#eXCHANGE TRADED only volume

# dir_OptionMarketStat_daily_webpage='./OptionMarketStat_daily'
# _url_OptionMarketStat_daily = "https://www.cboe.com/us/options/market_statistics/daily/"
# _savedName_webpage = "Cboe_OptionMarketStat_daily.html"


#--------table name ---------
# _sqlTable_PutCall_ratio_A = 'PutCall_ratio_A'  
# _sqlTable_PutCall_ratio_B = 'PutCall_ratio_B'

import key as pconst
_server = pconst.RYAN_SQL['server']
_username = pconst.RYAN_SQL['username']
_password = pconst.RYAN_SQL['password']  
_database = 'Cboe' 


pd.set_option('mode.chained_assignment', None)





def makeTodayDataDir(newDir):
    # if not myPath.lexists(newDir): #lexists
    if not myPath.exists(newDir):
        makedirs(newDir)

def convert_dateStr(MMMMddyyyy):
    return datetime.strptime(MMMMddyyyy, '%B %d, %Y').strftime('%Y-%m-%d')

def convert_dateStr_2019(MMMMddyyyy):
    return datetime.strptime(MMMMddyyyy, '%A, %B %d, %Y').strftime('%Y-%m-%d')
        
def convertDDMM_date(MMMdd):
    timeRef = constA.todayDate_str
    yy = timeRef.split('-')
    year = yy[0]
    year1 = str(int(year) - 1)  

    dateStr = MMMdd + ' ' + year 
    dateStr1 = MMMdd + ' ' + year1 
    yy = datetime.strptime(dateStr, '%b %d %Y').strftime('%Y-%m-%d')
    if yy <= timeRef:
        return yy
    else:
        return datetime.strptime(dateStr1, '%d %b %Y').strftime('%Y-%m-%d')        

def isSP500_SPX(text):
    if 'S and P 500 Index - (SPX)'.lower() in text.lower():
        return True
    elif 'S&P 500 INDEX - (SPX)'.lower() in text.lower():
        return True
    elif 'S&P 500 INDEX (SPX)'.lower() in text.lower():
        return True
    else:
        return False
    
def isSP500_SPX_Weekly(text):
    if 'S AND P 500 INDEX WEEKLYS'.lower() in text.lower().strip():
        return True
    elif 'S&P 500 INDEX WEEKLYS'.lower() in text.lower().strip():
        return True
    elif 'S&P 500 INDEX - PM SETTLED (SPXW)'.lower() in text.lower().strip():
        return True
    else:
        return False
    
# def isRUT(text):
#     if '(rut)'.lower() in text.lower().strip():
#         return True
#     elif 'RUSSELL 2000 INDEX'.lower() in text.lower().strip():
#         return True
#     # elif 'S&P 500 INDEX - PM SETTLED (SPXW)'.lower() in text.lower().strip():
#     #     return True
#     else:
#         return False

def extractData_sum(htmlFileFullPath, dest_fileFullPath): 
    # soup = BeautifulSoup(htmlFileFullPath, 'html.parser')
    # soup = BeautifulSoup(htmlFileFullPath, 'lxml')
    page = open(htmlFileFullPath)
    soup = BeautifulSoup(page, 'lxml')
    # soup = BeautifulSoup(page.read())
    
    page.close()
    
    cols = ["Vol_oi","Call", "Put", "Total", "empty"]    
    df = pd.DataFrame(columns = cols)
    
    #date 
    items = soup.find("span" , attrs = {'id': 'ContentTop_ctl09_m_labReportDate'}) 
    dateStr = convert_dateStr_2019(items.text)
    print (dateStr)
    
    tableTop = soup.find('table', attrs = {'id' : 'ContentTop_ctl09_tblMktStatsFirstSummary'})
    table = tableTop.find('table', {'class': 'overview'})
                          
    trs = table.find_all('tr')
    for i in range(len(trs)): 
        l = []
        if "sum of all products" == (trs[i].text).strip().lower():
            # print("---" + trs[i].text) # Head 1
            # print (trs[i+1].text) # Head 2
            tds_volume  = trs[i+2].find_all('td')
            tds_oi      = trs[i+3].find_all('td')
            # print (tds_volume[0].text, tds_volume[1].text)            
            row_volume = [tr.text for tr in tds_volume]
            row_oi      = [tr.text for tr in tds_oi]
            
            l.append(row_volume)
            l.append(row_oi)
            
            df1 = pd.DataFrame(l, columns = cols) 
            
            df1.insert(0,'Name',"sum of all products")
            df1.insert(0,'Date',dateStr)
            df = df1[df1.columns[:-1]]
            
            df.to_csv(dest_fileFullPath, mode='a', header = False, index= False)
                        
            break

   
# htmlFileFullPath = "G://Projects//HFinvest//Cboe//OptionCbeoOnly_history_VolOI//2003//2003-10-28//Cboe_OptionMarketStat_daily.html"

# htmlFileFullPath = "./OptionCbeoOnly_history_VolOI//2019//2019-01-02//Cboe_OptionMarketStat_daily.html"
# dest_fileFullPath = _dir_Option_CbeoOnly_history + _fileName_sum
# extractData_sum(htmlFileFullPath, dest_fileFullPath)


def extractData_keyword(htmlFileFullPath, dest_fileFullPath, keyword): 
    # soup = BeautifulSoup(htmlFileFullPath, 'html.parser')
    # soup = BeautifulSoup(htmlFileFullPath, 'lxml')
    page = open(htmlFileFullPath)
    soup = BeautifulSoup(page, 'lxml')
    # soup = BeautifulSoup(page.read())
    
    page.close()
    
    cols = ["Vol_oi","Call", "Put", "Total", "empty"]    
    df = pd.DataFrame(columns = cols)
    
    #date 
    items = soup.find("span" , attrs = {'id': 'ContentTop_ctl09_m_labReportDate'}) 
    dateStr = convert_dateStr_2019(items.text)
    
    
    tableTop = soup.find('table', attrs = {'id' : 'ContentTop_ctl09_tblMktStatsProductsSummary'})
    # table = tableTop.find('table', {'class': 'overview'})
    table = tableTop.find('table')
    # span id = "OEX" 2019 2003
    # OI id = "ContentTop_ctl09_ctl37_tr3DatVal" 2019
             # ContentTop_ctl09_ctl33_tr3DatVal  2016
            # "ContentTop_ctl09_ctl21_tr3DatVal " 2003           
    trs = table.find_all('tr')
    for i in range(len(trs)): 
        l = []
        if keyword in (trs[i].text).strip().lower():
            # print("---" + trs[i].text) # Head 1
            # print (trs[i+1].text) # Head 2
            tds_volume  = trs[i+2].find_all('td')
            tds_oi      = trs[i+3].find_all('td')
            # print (tds_volume[0].text, tds_volume[1].text)            
            row_volume = [tr.text for tr in tds_volume]
            row_oi      = [tr.text for tr in tds_oi]
            
            l.append(row_volume)
            l.append(row_oi)
            
            df1 = pd.DataFrame(l, columns = cols) 
            
            df1.insert(0,'Name',(trs[i].text).strip())
            df1.insert(0,'Date',dateStr)
            df = df1[df1.columns[:-1]]
            
            df.to_csv(dest_fileFullPath, mode='a', header = False, index= False)
            
            print (dateStr)            
            break

# htmlFileFullPath = "./OptionCbeoOnly_history_VolOI//history_all_webpage_working1//2019//2019-01-02//Cboe_OptionMarketStat_daily.html"
# dest_fileFullPath = _dir_Option_CbeoOnly_history + _fileName_oex
# keyword = _oexKey
# name = "SP100_OEX"
# extractData_keyword(htmlFileFullPath, dest_fileFullPath, keyword, name)
# print()
    
def extractData_No_keyword(htmlFileFullPath, dest_fileFullPath): 
    page = open(htmlFileFullPath)
    soup = BeautifulSoup(page, 'lxml')
    page.close()
    
    cols = ["Vol_oi","Call", "Put", "Total", "empty"]    
    df = pd.DataFrame(columns = cols)
    
    #date 
    items = soup.find("span" , attrs = {'id': 'ContentTop_ctl09_m_labReportDate'}) 
    dateStr = convert_dateStr_2019(items.text)    
    
    tableTop = soup.find('table', attrs = {'id' : 'ContentTop_ctl09_tblMktStatsProductsSummary'})
    # table = tableTop.find('table', {'class': 'overview'})
    table = tableTop.find('table')
          
    trs = table.find_all('tr')
    for i in range(len(trs)): 
        l = []
        
        # if isSP500_SPX(trs[i].text) :
        if isSP500_SPX_Weekly(trs[i].text) :
            # print("---" + trs[i].text) # Head 1
            # print (trs[i+1].text) # Head 2
            tds_volume  = trs[i+2].find_all('td')
            tds_oi      = trs[i+3].find_all('td')
            # print (tds_volume[0].text, tds_volume[1].text)            
            row_volume = [tr.text for tr in tds_volume]
            row_oi      = [tr.text for tr in tds_oi]
            
            l.append(row_volume)
            l.append(row_oi)
            
            df1 = pd.DataFrame(l, columns = cols) 
            
            df1.insert(0,'Name',trs[i].text.strip())
            df1.insert(0,'Date',dateStr)
            df = df1[df1.columns[:-1]]
            
            df.to_csv(dest_fileFullPath, mode='a', header = False, index= False)
            
            print (dateStr)            
            break
     

    

# def sql_Cboe_OptionMarketStat_daily_HTML_putCallRatio_before2012_06(htmlFileFullPath):
#     myDataFrameLists = pd.read_html(htmlFileFullPath, attrs={"id": "ContentTop_ctl09_lvMktStatsRatios_tabMktStatsRatios"})   
#     if len(myDataFrameLists) == 0:
#         msg = "empty Cbeo option market stat daily table from website: " + htmlFileFullPath
#         mydownPy.logError(errorFileTargetDir, msg)  
#         return
#     else: 
#         htmlFilePath = constA.getFilePathInfo(htmlFileFullPath, 0)
#         # metalName    = constA.getFilePathInfo(htmlFileFullPath, 2).strip()
#         date_fromFolderName  = constA.getFilePathInfo(htmlFilePath, 1) 
#         # df_ratio = ((myDataFrameLists[0]).iloc[1:6, 2:4]).copy()  
#         df_ratio = ((myDataFrameLists[0]).iloc[ [1,2,3,4], [2,3]])
#         df_ratio.reset_index()        
#         # ----- ration  ---- connect the database        
#         cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server+';DATABASE='+_database+';UID='+_username+';PWD='+_password)
#         cursor = cnxn.cursor()  
        
#         #----the dataframe change it becomes data[2,3]
#         for (index, data) in df_ratio.iterrows(): 
#             date_del = date_fromFolderName
#             rationName = data[2]             
#             query = """DELETE FROM %s where Date = '%s' and Name = '%s' ;""" % (_sqlTable_PutCall_ratio_A, date_del, rationName)
#             cursor.execute(query)
            
#             params =  tuple([date_fromFolderName, rationName, data[3]])            
#             # print (params)
#             # print (htmlFileFullPath)            
#             query = """INSERT INTO %s VALUES (?,?,? );""" %(_sqlTable_PutCall_ratio_A)
#             cursor.execute(query, params)

#         cnxn.commit()
#         print ("Cbeo putCallRatio sql:  " + date_fromFolderName)        
#         # -----close database connection ----------
#         cursor.close()
#         cnxn.close()    
# # htmlFileFullPath = 'G:\\Projects\\HFinvest\\Cboe\\2019\\2019-01-02\\Cboe_OptionMarketStat_daily.html'
# # sql_Cboe_OptionMarketStat_daily_HTML_putCallRatio_before2012_06(htmlFileFullPath)
# # print()

# def sql_Cboe_OptionMarketStat_daily_HTML_putCallRatio(htmlFileFullPath):
#     myDataFrameLists = pd.read_html(htmlFileFullPath, attrs={"id": "ContentTop_ctl09_lvMktStatsRatios_tabMktStatsRatios"})   
#     if len(myDataFrameLists) == 0:
#         msg = "empty Cbeo option market stat daily table from website: " + htmlFileFullPath
#         mydownPy.logError(errorFileTargetDir, msg)  
#         return
#     else: 
#         htmlFilePath = constA.getFilePathInfo(htmlFileFullPath, 0)
#         # metalName    = constA.getFilePathInfo(htmlFileFullPath, 2).strip()
#         date_fromFolderName  = constA.getFilePathInfo(htmlFilePath, 1) 
#         # df_ratio = ((myDataFrameLists[0]).iloc[1:6, 2:4]).copy()  
#         df_ratio = ((myDataFrameLists[0]).iloc[ [1,2,3,4,5], [2,3]])
#         df_ratio.reset_index()        
#         # ----- ration  ---- connect the database        
#         cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server+';DATABASE='+_database+';UID='+_username+';PWD='+_password)
#         cursor = cnxn.cursor()  
        
#         #----the dataframe change it becomes data[2,3]
#         for (index, data) in df_ratio.iterrows(): 
#             date_del = date_fromFolderName
#             rationName = data[2]             
#             query = """DELETE FROM %s where Date = '%s' and Name = '%s' ;""" % (_sqlTable_PutCall_ratio_A, date_del, rationName)
#             cursor.execute(query)
            
#             params =  tuple([date_fromFolderName, rationName, data[3]])            
#             # print (params)
#             # print (htmlFileFullPath)            
#             query = """INSERT INTO %s VALUES (?,?,? );""" %(_sqlTable_PutCall_ratio_A)
#             cursor.execute(query, params)

#         cnxn.commit()
#         print ("Cbeo putCallRatio sql:  " + date_fromFolderName)        
#         # -----close database connection ----------
#         cursor.close()
#         cnxn.close()    
# # htmlFileFullPath = 'G:\\Projects\\HFinvest\\Cboe\\2019\\2019-01-02\\Cboe_OptionMarketStat_daily.html'
# # sql_Cboe_OptionMarketStat_daily_HTML_putCallRatio(htmlFileFullPath)
# # print()


# def sql_Cboe_OptionMarketStat_daily_HTML_vol_OpenInterest(htmlFileFullPath):
#     myDataFrameLists = pd.read_html(htmlFileFullPath)   
#     if len(myDataFrameLists) == 0:
#         msg = "empty Cbeo option market stat daily table from website: " + htmlFileFullPath
#         mydownPy.logError(errorFileTargetDir, msg)  
#         return
#     else: 
#         htmlFilePath = constA.getFilePathInfo(htmlFileFullPath, 0)
#         # metalName    = constA.getFilePathInfo(htmlFileFullPath, 2).strip()
#         date_fromFolderName  = constA.getFilePathInfo(htmlFilePath, 1) 

#         # ----- ration  ---- connect the database        
#         cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server+';DATABASE='+_database+';UID='+_username+';PWD='+_password)
#         cursor = cnxn.cursor() 
        
#         #  tables from 1 to last
#         for count in range (1, len(myDataFrameLists)): 
#             df = myDataFrameLists[count]
#             volOIName = df.columns[0]
#             params = (date_fromFolderName, volOIName)
            
#             count = 0
#             for (columnName, columnData) in df.iteritems():
#                 if count == 0:
#                     count +=1
#                     continue               
#                 date_del = date_fromFolderName
#                 optionType = columnData[0]                
#                 query = """DELETE FROM %s where Date = '%s' and Name = '%s' and OptionType = '%s';""" % (_sqlTable_PutCall_ratio_B, date_del, volOIName, optionType)
#                 cursor.execute(query)
#                 # print (query)
#                 params1 = tuple(columnData)
#                 params2 =  params + params1 
#                 # print (params2 + "  " + htmlFileFullPath)
#                 query = """INSERT INTO %s VALUES (?,?,?,?,?);""" %(_sqlTable_PutCall_ratio_B)
#                 cursor.execute(query, params2)
#                 # print (params2)
#         cnxn.commit()
#         print ("Cbeo volume openInterest sql:  " + date_fromFolderName)        
#         # -----close database connection ----------
#         cursor.close()
#         cnxn.close()       
# # htmlFileFullPath = dir_OptionMarketStat_daily_webpage +'/2021-10-04/Cboe_OptionMarketStat_daily.html'
# # sql_Cboe_OptionMarketStat_daily_HTML_vol_OpenInterest(htmlFileFullPath)
# # print()

def loadAllFiles():
    # sourceDir = "G:\\Projects\\HFinvest\\Cboe\\OptionCbeoOnly_history_VolOI\\history_all_webpage_working1"
    # sourceDir = "G:\\Projects\\HFinvest\\Cboe\\OptionCbeoOnly_history_VolOI\\history_all_webpage_working2"
    sourceDir = "G:\\Projects\\HFinvest\\Cboe\\OptionCbeoOnly_history_VolOI\\history_all_webpage_working3"
    # sourceDir = "G:\\Projects\\HFinvest\\Cboe\\OptionCbeoOnly_history_VolOI\\history_all_webpage"
    # sourceDir = "G:\\Projects\\HFinvest\\Cboe\\OptionCbeoOnly_history_VolOI\\history_all_webpage_Backup"


    # pathlist = Path(sourceDir).glob('**/*.html')
    pathlist = Path(sourceDir).glob('**/Cboe_OptionMarketStat_daily.html')    
    for path in pathlist:
         # because path is object not string
         # print(path)
         htmlFileFullPath = str(path)
   # -------sum
        # dest_fileFullPath = _dir_Option_CbeoOnly_history + _fileName_sum
         # extractData_sum(htmlFileFullPath, dest_fileFullPath)

   # # ---OEX
   #       dest_fileFullPath = _dir_Option_CbeoOnly_history + _fileName_vix
   #       keyword = _vixKey
   #       name = "cboe volatility index options"
   #       extractData_keyword(htmlFileFullPath, dest_fileFullPath, keyword)

   # ---SPXW  or spx
         # dest_fileFullPath = _dir_Option_CbeoOnly_history + _fileName_SPX
         # dest_fileFullPath = _dir_Option_CbeoOnly_history + _fileName_SPXW
         # extractData_No_keyword(htmlFileFullPath, dest_fileFullPath)   

    # ---RUT
         dest_fileFullPath = _dir_Option_CbeoOnly_history + _fileName_rut
         keyword = _rutKey
         extractData_keyword(htmlFileFullPath, dest_fileFullPath, keyword)
         
loadAllFiles() 

   

  
						
