# -*- coding: utf-8 -*-
"""
@author: haoli
"""
import sys
sys.path.append("../")
# import const_common as constA
# import downloadUpdateData as mydownPy

import downloadUpdateData as mydownPy

from datetime import datetime
# from datetime import timedelta
# import requests
# from os import makedirs

# import os.path as myPath
import pandas as pd

# from urllib.request import urlopen, Request
# from pathlib import Path 
import os

import pyodbc
import numpy as np

import time
from selenium import webdriver
# from selenium.common.exceptions import NoSuchElementException
import ntpath

import pyautogui #, time
pyautogui.PAUSE =2.5

from pathlib import Path
# import requests
# from bs4 import BeautifulSoup
# import re

#----------------------------------
errorFileTargetDir = '../'
# mydownPy.logError("my test message")
#logError(errorFileTargetDir, msg)
# mydownPy.logError(errorFileTargetDir, "my test message")

# _dir_EquityMarketStat_daily_Vol             = './EquityMarketStat_daily\\Volume'
# _dir_EquityMarketStat_daily_TradingValue    = './EquityMarketStat_daily\\TradingValue'



# _url_OptionMarketStat_daily = "https://www.cboe.com/us/options/market_statistics/daily/"
# _savedName_webpage = "Cboe_OptionMarketStat_daily.html"

# _url_EquityMarketStat_daily = "https://www.cboe.com/us/equities/market_statistics/market/"

_url_EquityTradingValueVol_daily = "https://www.cboe.com/us/equities/market_statistics/historical_market_volume/"
_dir_EquityTradingValueVol_daily = './EquiptyTrading_ValueVolume_daily'

#--------table name ---------
_sqlTable_EquiptyTrading_ValueVolume_daily = 'EquiptyTrading_ValueVolume_daily'


import key as pconst
_server = pconst.RYAN_SQL['server']
_username = pconst.RYAN_SQL['username']
_password = pconst.RYAN_SQL['password']  
_database = 'Cboe' 

pd.set_option('mode.chained_assignment', None)

# from dateutil.rrule import rrule, MONTHLY
# from datetime import datetime

def save_EquityMarketStat_csvFile_daily_Volume(url, dir_destFile): 
    prefs = {#"download.default_directory" : winPath,
            "download.prompt_for_download": True,
            "download.directory_upgrade": True,
            "safebrowsing_for_trusted_sources_enabled": False,
            "safebrowsing.enabled": False,            
            'download.manager.showWhenStarting': True,
            'helperApps.neverAsk.saveToDisk': 'text/csv/xls, application/vnd.ms-excel, application/octet-stream'
             }  #("network.http.response.timeout", 30)     
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_experimental_option("prefs",prefs)     
    driver = webdriver.Chrome('../chromedriver.exe', options= chromeOptions)
    driver.implicitly_wait(10)
    
    driver.get(url)
    time.sleep(3)
    # accept cookie
    # driver.find_element_by_xpath("/html/body/div[3]/div[2]/div/div/button").click()
    driver.find_element_by_xpath("//html/body/div[3]/div[1]/div/div/button[2]").click()
    time.sleep(2)

    elems = driver.find_elements_by_tag_name('a')
    time.sleep(1)
  
    isLink = False
    for elem in elems:        
        # href = elem.get_attribute('href')    
        str_InText = 'market_history_' + str(datetime.now().year)
        if str_InText in (elem.text).lower(): # if str_Inhref in href: # is not None: 
            fileName = elem.get_attribute('text')        
            # fileName = elem.text
            # print(href)            
            elem.click()
            isLink= True
            break
    if isLink :
        pass
    else:
        print ("Error:  No data - Cboe Equity Market Stat ")
        return ""
    
    # # -------- make file dir, delete old file and set the file name   
    # makeTodayDataDir(destFilePath)
    fileFullPath = dir_destFile + '/' + fileName
    if os.path.isfile(fileFullPath):
        os.remove(fileFullPath)
        print('file removed: ' + fileFullPath)
        time.sleep(5)
        
    #-----convert python dir to windows dir 
    fileAbsPath = os.path.abspath(fileFullPath)   
    winPath = fileAbsPath.replace(os.sep,ntpath.sep)    
    time.sleep(1)
    pyautogui.typewrite(winPath)
    time.sleep(2)
    
    pyautogui.hotkey('enter')
    time.sleep(5) #wait for download finish
   
    driver.quit() 
    print("Equity Market value and volume daily csv:  " +  fileFullPath)
    return fileFullPath 

# url = _url_EquityTradingValueVol_daily
# dir_destFile = _dir_EquityTradingValueVol_daily
# a = save_EquityMarketStat_csvFile_daily_Volume(url, dir_destFile)
# print(a)

def sql_Cboe_EquityMarketStat_csvFile_daily_TradingValue(csvFileFullPath, databaseName, isLoadLast10):
    df = pd.read_csv(csvFileFullPath)
    
    df["Total sharePerCount"] = df["Total Shares"] / (df["Total Trade Count"] +0.01)
    df["Total notionalPerCount"] = df["Total Notional"] / (df["Total Trade Count"] +0.01)
    
    df = df.replace({np.NAN: None}) 
    if len(df) == 0:
        msg = "empty Cbeo equity volume market stat daily: " + csvFileFullPath
        mydownPy.logError(errorFileTargetDir, msg)  
        return
    else:         
        # ----- ration  ---- connect the database        
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server+';DATABASE='+_database+';UID='+_username+';PWD='+_password)
        cursor = cnxn.cursor()  
        
        count = 0
        for (index, data) in df.iterrows(): 
            date_del = data[0]            
            # MarketParticipant = data[1]            
            # query = """DELETE FROM %s where Date = '%s' and [Market Participant] = '%s' ;""" % (databaseName, date_del, MarketParticipant)
            TotalShares = data[5]            
            query = """DELETE FROM %s where Date = '%s' and [Total Shares] = %s ;""" % (databaseName, date_del, TotalShares)
            cursor.execute(query)
            
            params =  tuple(data)            
            # print (params)          
            query = """INSERT INTO %s VALUES (?,?,?,?,?, ?,?,?,?,?, ?,?,?,?,?,  ?);""" %(databaseName)
            cursor.execute(query, params)
            if (isLoadLast10) :
                count +=1
                if count >200:
                    break  
        cnxn.commit()
        print ("Cbeo Market trading Volume sql:  " + csvFileFullPath)  
        # -----close database connection ----------
        cursor.close()
        cnxn.close()    
# csvFileFullPath = 'G:\\Projects\\HFinvest\\Cboe\\EquiptyTrading_ValueVolume_daily\\market_history_2022.csv'
# databaseName = _sqlTable_EquiptyTrading_ValueVolume_daily
# sql_Cboe_EquityMarketStat_csvFile_daily_TradingValue(csvFileFullPath, databaseName, True)
# print()

def loadAllFiles():
    sourceDir = "G:\\Projects\\HFinvest\\Cboe\\EquiptyTrading_ValueVolume_daily"
    # pathlist = Path(sourceDir).glob('**/*.html')
    pathlist = Path(sourceDir).glob('**/*.csv')    
    for path in pathlist:
         # because path is object not string
         # print(path)
         csvFileFullPath = str(path)         
         databaseName = _sqlTable_EquiptyTrading_ValueVolume_daily
         sql_Cboe_EquityMarketStat_csvFile_daily_TradingValue(csvFileFullPath, databaseName, False)    
# loadAllFiles() 


def Cboe_EquityMarketStat_daily_run():
    url = _url_EquityTradingValueVol_daily
    dir_destFile = _dir_EquityTradingValueVol_daily
    csvFileFullPath = save_EquityMarketStat_csvFile_daily_Volume(url, dir_destFile)
    
    if (csvFileFullPath == ""):
        return
    
    databaseName = _sqlTable_EquiptyTrading_ValueVolume_daily
    isLoadLast10 = True
    sql_Cboe_EquityMarketStat_csvFile_daily_TradingValue(csvFileFullPath, databaseName, isLoadLast10)

Cboe_EquityMarketStat_daily_run()



  

   

  
						
