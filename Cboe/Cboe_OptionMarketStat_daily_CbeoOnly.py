# -*- coding: utf-8 -*-
"""
@author: haoli
"""
import sys
sys.path.append("../")
import const_common as constA
# import downloadUpdateData as mydownPy

# import downloadUpdateData as mydownPy

from datetime import datetime
from datetime import timedelta
# import requests
from os import makedirs

import os.path as myPath
import pandas as pd

# from urllib.request import urlopen, Request
# from pathlib import Path 
import os

import pyodbc
import numpy as np

import time
from selenium import webdriver

# import ntpath

import pyautogui #, time
pyautogui.PAUSE =2.5

# from pathlib import Path

# import requests
# from bs4 import BeautifulSoup
# import re

#----------------------------------
errorFileTargetDir = '../'
# mydownPy.logError("my test message")
#logError(errorFileTargetDir, msg)
# mydownPy.logError(errorFileTargetDir, "my test message")

dir_Option_CbeoOnly_daily          = './OptionCbeoOnly_daily'
# dir_OptionMarketStat_daily          = './OptionMarketStat_daily'
# dir_OptionMarketStat_daily_webpage  = './OptionMarketStat_daily'

_url_OptionMarketStat_daily = "https://www.cboe.com/us/options/market_statistics/daily/"
# _savedName_webpage = "Cboe_OptionMarketStat_daily.html"


#--------table name ---------
_sqlTable_Option_CboeSum_daily      = 'Option_CboeSum_daily'
_sqlTable_Option_CboeIndex_daily    = 'Option_CboeIndex_daily'
_sqlTable_Option_CboeExchangeTradeProduct_daily      = 'Option_CboeExchangeTradeProduct_daily'
_sqlTable_Option_CboeEquity_daily   = 'Option_CboeEquity_daily'
_sqlTable_Option_CboeVOLATILITYINDEX_daily          = 'Option_CboeVOLATILITYINDEX_daily'
_sqlTable_Option_CboeSPX_daily      = 'Option_CboeSPX_daily'
_sqlTable_Option_CboeOEX_daily      = 'Option_CboeOEX_daily'
_sqlTable_Option_CboeMRUT_daily     = 'Option_CboeMRUT_daily'

# _sqlTable_PutCall_ratio_A = 'PutCall_ratio_A'  
# _sqlTable_PutCall_ratio_B = 'PutCall_ratio_B_Vol_OI'
_PCratio = "ratios"
_sum = "sum of all products"
_index = "index options"
_ETP = "exchange traded products"
_equity= "equity options"
# _VIX = "vix"
_VIX = "cboe volatility index (vix)" #"VOLATILITY INDEX"
_SPX = "spx + spxw"
_OEX = "oex"
_MRUT = "mrut"
_RUT = "rut"

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
    try:
        return datetime.strptime(MMMMddyyyy, '%B %d, %Y').strftime('%Y-%m-%d')
    except ValueError:
        return ""    

def convert_dateStr_2019(MMMMddyyyy):
    try:
        return datetime.strptime(MMMMddyyyy, '%A, %B %d, %Y').strftime('%Y-%m-%d')
    except ValueError:
        return ""          
        
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

def date_1yr_pre(yymmdd_str):
    yy = yymmdd_str.split('-')
    year = int(yy[0]) - 1
    dateStr = str(year) + '-' + yy[1] + '-' + yy[2]
    return dateStr

def getDatabaseName(colName):
    if _sum in colName.lower():
        return _sqlTable_Option_CboeSum_daily
    elif _index in colName.lower():
        return _sqlTable_Option_CboeIndex_daily    
    elif _ETP in colName.lower():
        return _sqlTable_Option_CboeExchangeTradeProduct_daily    
    elif _equity in colName.lower():
        return _sqlTable_Option_CboeEquity_daily    
    elif _VIX in colName.lower():
        return _sqlTable_Option_CboeVOLATILITYINDEX_daily    
    elif _SPX in colName.lower():
        return _sqlTable_Option_CboeSPX_daily    
    elif _OEX in colName.lower():
        return _sqlTable_Option_CboeOEX_daily    
    elif _MRUT in colName.lower()  or _RUT in colName.lower():
        return _sqlTable_Option_CboeMRUT_daily
    elif _PCratio in colName.lower():
        return _PCratio       
    else:
        return ""

def saveWebPage_OptionCboeOnly_daily(url, dir_destFile): 
    driver = webdriver.Chrome('../chromedriver.exe')
    driver.implicitly_wait(10)    
    driver.get(url)
    time.sleep(3)

    #--- agreemnet 
    driver.find_element_by_xpath("/html/body/div[3]/div[2]/div/div/button").click()
    time.sleep(2)    
#https://stackoverflow.com/questions/47828481/convert-dynamically-loaded-table-into-pandas-dataframe 
# soup = BeautifulSoup(htmlSource, 'html.parser')
# table = soup.find('div', class_='ngs-data-table')   
    # r = requests.get(url)
    # time.sleep(5)
    # soup =   BeautifulSoup(r.content,"lxml")
    # tables = soup.find_all('table') 
    # for table in tables:
    #     df = pd.read_html(str(table))    
    
    #------get Data and date---  
    tables = pd.read_html(driver.page_source)
    if (len(tables) == 0) :
        print ("error:  No Table found.  " + url)
        driver.quit() 
        return "no table"
    # check the date   
    # /html/body/div/div[2]/div[4]/table[2]/tbody/tr/td/div/table/tbody/tr/td/table/tbody/tr/td/h2/span                      
    # /html/body/div/div[2]/div[4]/table[2]/tbody/tr/td/div/table/tbody/tr/td/table/tbody/tr/td/h2/span
    dateLine = driver.find_element_by_xpath("/html/body/main/section/div/div[1]/div/div/div/button/span[2]")
    # dateLine = driver.find_element_by_id("calendarbutton-1009-btnInnerEl")
    # print(dateLine.text) Button__TextContainer-sc-1tdgwi0-1 hFHkoL
    dateStr = convert_dateStr((dateLine.text))
    if dateStr == "":
        print("error:  No date found.  " + url)
        driver.quit() 
        return "no date" 
    
    destFilePath = dir_destFile + '/' + dateStr     
    # -------- make file dir, delete old file and set the file name   
    makeTodayDataDir(destFilePath)   
     
    driver.quit()    
    time.sleep(1)

    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server+';DATABASE='+_database+';UID='+_username+';PWD='+_password)
    cursor = cnxn.cursor() 
        
    for df in tables:
        databaseName = getDatabaseName(df.columns[0])
        if databaseName == "":
            print ("error:   This table is new:  " + df.columns[0])
            # print (df)
            # continue 
            fileFullPath = destFilePath + '/' + df.columns[0] + ".csv"
        else:        
            fileFullPath = destFilePath + '/' + databaseName + ".csv"
            
        if os.path.isfile(fileFullPath):
            os.remove(fileFullPath)
            print('file removed: ' + fileFullPath)
            time.sleep(1)
            
        df.insert(0,'Date',dateStr)
        df.to_csv(fileFullPath, index=False)      # print(databaseName)        
        print (" --- Option CBOE only daily webpage saved: " + databaseName)
        
        # save df to database
        if databaseName == _PCratio or databaseName == "": #not used
            continue    
        df = df.replace({np.NAN: None}) 
        query = """DELETE FROM %s where Date = '%s';""" % (databaseName, dateStr)
        cursor.execute(query)
        
        for (index, data) in df.iterrows(): 
            cName = data[1]
            if cName is None:
                continue
            if "volume" in cName.lower() or "open interest" in cName.lower():            
                params =  tuple(data)            
                query = """INSERT INTO %s VALUES (?,?,?,?,? );""" %(databaseName)
                cursor.execute(query, params)
        cnxn.commit()
        # print ("--- Option CBOE only daily data sql:  " + databaseName)        
    
    # -----close database connection ----------
    cursor.close()
    cnxn.close()  
    return "True"
# url = _url_OptionMarketStat_daily
# dir_destFile = dir_Option_CbeoOnly_daily
# saveWebPage_OptionCboeOnly_daily(url, dir_destFile)
# print() 

def download_perod_ofDays(): 
    # date_list1 = [datetime.strptime('2019-10-07', "%Y-%m-%d") + timedelta(days=x) for x in range(85)]    
    # date_list2 = [datetime.strptime('2020-01-02', "%Y-%m-%d") + timedelta(days=x) for x in range(365)]    
    date_list2 = [datetime.strptime('2020-08-13', "%Y-%m-%d") + timedelta(days=x) for x in range(141)]    
    date_list3 = [datetime.strptime('2021-01-02', "%Y-%m-%d") + timedelta(days=x) for x in range(363)]    
    
    date_list_a = [date_list2, date_list3]
    for dList in range(len(date_list_a)):
        date_list = date_list_a[dList]
        # print(date_list)
        for d in date_list:
            if d.weekday() == 5 or d.weekday() == 6:
                print ("weekend: " +  d.strftime("%Y-%m-%d"))
                continue  
            url1 = "https://www.cboe.com/us/options/market_statistics/daily/?dt=" 
            url2 = d.strftime("%Y-%m-%d")        
            url = url1 + url2            
            
            dir_destFile = dir_Option_CbeoOnly_daily
            msg = saveWebPage_OptionCboeOnly_daily(url, dir_destFile)
            if msg == "True":
                print ("download:  " + d.strftime("%Y-%m-%d"))
            else:
                print ("------" + d.strftime("%Y-%m-%d"))     
# download_perod_ofDays()


def Cbeo_OptionMarketStat_CboeOnly_daily():    
    url = _url_OptionMarketStat_daily
    dir_destFile = dir_Option_CbeoOnly_daily
    saveWebPage_OptionCboeOnly_daily(url, dir_destFile)

Cbeo_OptionMarketStat_CboeOnly_daily()




  
						
