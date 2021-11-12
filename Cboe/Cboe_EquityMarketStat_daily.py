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
import numpy as np

import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
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

_dir_EquityMarketStat_daily_Vol             = './EquityMarketStat_daily\\Volume'
_dir_EquityMarketStat_daily_TradingValue    = './EquityMarketStat_daily\\TradingValue'

_url_EquityMarketStat_daily = "https://www.cboe.com/us/equities/market_statistics/market/"


# _url_OptionMarketStat_daily = "https://www.cboe.com/us/options/market_statistics/daily/"
# _savedName_webpage = "Cboe_OptionMarketStat_daily.html"





#--------table name ---------
_sqlTable_EquiptyVolume_daily = 'EquiptyVolume_daily'  
_sqlTable_EquiptyTradingValue_daily = 'EquiptyTradingValue_daily'

import key as pconst
_server = pconst.RYAN_SQL['server']
_username = pconst.RYAN_SQL['username']
_password = pconst.RYAN_SQL['password']  
_database = 'Cboe' 


pd.set_option('mode.chained_assignment', None)


from dateutil.rrule import rrule, MONTHLY

from dateutil.rrule import rrule, MONTHLY
from datetime import datetime


def makeTodayDataDir(newDir):
    # if not myPath.lexists(newDir): #lexists
    if not myPath.exists(newDir):
        makedirs(newDir)

def convert_dateStr(MMMMddyyyy):
    return datetime.strptime(MMMMddyyyy, '%B %d, %Y').strftime('%Y-%m-%d')

# def convert_dateStr_2019(MMMMddyyyy):
#     return datetime.strptime(MMMMddyyyy, '%A, %B %d, %Y').strftime('%Y-%m-%d')
        
# def convertDDMM_date(MMMdd):
#     timeRef = constA.todayDate_str
#     yy = timeRef.split('-')
#     year = yy[0]
#     year1 = str(int(year) - 1)  

#     dateStr = MMMdd + ' ' + year 
#     dateStr1 = MMMdd + ' ' + year1 
#     yy = datetime.strptime(dateStr, '%b %d %Y').strftime('%Y-%m-%d')
#     if yy <= timeRef:
#         return yy
#     else:
#         return datetime.strptime(dateStr1, '%d %b %Y').strftime('%Y-%m-%d')        

# def date_1yr_pre(yymmdd_str):
#     yy = yymmdd_str.split('-')
#     year = int(yy[0]) - 1
#     dateStr = str(year) + '-' + yy[1] + '-' + yy[2]
#     return dateStr
# # calendarbutton-1009-btnInnerEl

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
    driver.find_element_by_xpath("/html/body/div[3]/div[1]/div/div/button[2]").click()
    time.sleep(2)

    # find the date
    dateLine = driver.find_element_by_id("calendarbutton-1009-btnInnerEl")
    dateStr = dateLine.text
    # destFileName = dateStr
    
    # # -------- make file dir, delete old file and set the file name   
    # makeTodayDataDir(destFilePath)
    fileFullPath = dir_destFile + '/' + dateStr + ".csv"
    # fileFullPath = destFilePath_2 + '/' + destFileName
    if os.path.isfile(fileFullPath):
        os.remove(fileFullPath)
        print('file removed: ' + fileFullPath)
        time.sleep(5)
        
    #-----convert python dir to windows dir 
    fileAbsPath = os.path.abspath(fileFullPath)   
    winPath = fileAbsPath.replace(os.sep,ntpath.sep)    
    
    #---- this day as csv    
    driver.find_element_by_id("ms-app__csv").click()
    time.sleep(3)
    
    pyautogui.hotkey('ctrl', 's')
    time.sleep(2)
    
    pyautogui.typewrite(winPath)
    time.sleep(2)
    
    pyautogui.hotkey('enter')
    time.sleep(3) #wait for download finish
   
    driver.quit() 
    print("Equity Market Stat daily csv:  " +  dateStr)
    return fileFullPath 
# url = _url_EquityMarketStat_daily
# dir_destFile = _dir_EquityMarketStat_daily_Vol
# save_EquityMarketStat_csvFile_daily_Volume(url, dir_destFile)
# print()

def sql_Cboe_EquityMarketStat_csvFile_daily_Volume(csvFileFullPath):
    df = pd.read_csv(csvFileFullPath)
    if len(df) == 0:
        msg = "empty Cbeo equity volume market stat daily: " + csvFileFullPath
        mydownPy.logError(errorFileTargetDir, msg)  
        return
    else: 
        
        # ----- ration  ---- connect the database        
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server+';DATABASE='+_database+';UID='+_username+';PWD='+_password)
        cursor = cnxn.cursor()  
        
        #----the dataframe change it becomes data[2,3]
        for (index, data) in df.iterrows(): 
            date_del = data[0]            
            TradingMarketCentre = data[2]             
            query = """DELETE FROM %s where Date = '%s' and TradingMarketCentre = '%s' ;""" % (_sqlTable_EquiptyVolume_daily, date_del, TradingMarketCentre)
            cursor.execute(query)
            
            params =  tuple(data)            
            # print (params)
            # print (htmlFileFullPath)            
            query = """INSERT INTO %s VALUES (?,?,?,?,?, ?,?,?,?,?, ?);""" %(_sqlTable_EquiptyVolume_daily)
            cursor.execute(query, params)

        cnxn.commit()
        print ("Cbeo Market trading Volume sql:  " + csvFileFullPath)        
        # -----close database connection ----------
        cursor.close()
        cnxn.close()    
# csvFileFullPath = 'G:\\Projects\\HFinvest\\Cboe\\EquityMarketStat_daily\\Volume\\2021-10-08.csv'
# sql_Cboe_EquityMarketStat_csvFile_daily_Volume(csvFileFullPath)
# print()


def sql_Cboe_EquityMarketStat_csvFile_daily_TradingValue(csvFileFullPath):
    df = pd.read_csv(csvFileFullPath)
    df = df.replace({np.NAN: None}) 
    if len(df) == 0:
        msg = "empty Cbeo equity volume market stat daily: " + csvFileFullPath
        mydownPy.logError(errorFileTargetDir, msg)  
        return
    else:         
        # ----- ration  ---- connect the database        
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server+';DATABASE='+_database+';UID='+_username+';PWD='+_password)
        cursor = cnxn.cursor()  
        
        #----the dataframe change it becomes data[2,3]
        for (index, data) in df.iterrows(): 
            date_del = data[0]            
            TradingMarketCentre = data[1]             
            query = """DELETE FROM %s where Date = '%s' and TradingMarketCentre = '%s' ;""" % (_sqlTable_EquiptyTradingValue_daily, date_del, TradingMarketCentre)
            cursor.execute(query)
            
            params =  tuple(data)            
            # print (params)
            # print (htmlFileFullPath)            
            query = """INSERT INTO %s VALUES (?,?,?,?,?, ?,?,?);""" %(_sqlTable_EquiptyTradingValue_daily)
            cursor.execute(query, params)

        cnxn.commit()
        print ("Cbeo Market trading Volume sql:  " + csvFileFullPath)        
        # -----close database connection ----------
        cursor.close()
        cnxn.close()    
# csvFileFullPath = 'G:\\Projects\\HFinvest\\Cboe\\EquityMarketStat_daily\\TradingValue\\2021-10-08.csv'
# sql_Cboe_EquityMarketStat_csvFile_daily_TradingValue(csvFileFullPath)
# print()

def loadAllFiles():
    sourceDir = "G:\\Projects\\HFinvest\\Cboe\\EquityMarketStat_daily\\Volume"
    # pathlist = Path(sourceDir).glob('**/*.html')
    pathlist = Path(sourceDir).glob('**/*.csv')    
    for path in pathlist:
         # because path is object not string
         # print(path)
         csvFileFullPath = str(path)
         sql_Cboe_EquityMarketStat_csvFile_daily_Volume(csvFileFullPath)
          
         # sql_Cboe_OptionMarketStat_daily_HTML_vol_OpenInterest(htmlFileFullPath)    
# loadAllFiles() 

def dataframeConvert(fileFullPath):
    df = pd.read_csv(fileFullPath)        
    for (columnName, columnData) in df.iteritems():
        if "$" in columnData[0]:
            df[columnName] = (df[columnName].str.strip("$").str.replace(',','') ).astype(float)
            pass
        elif "%" in columnData[0]:
            df[columnName] = (df[columnName].str.strip("%") ).astype(float)/100
        else:
            pass
    return df


def save_EquityMarketStat_daily_TradingValue(url, dir_destFile):
    driver = webdriver.Chrome('../chromedriver.exe')
    driver.implicitly_wait(10)
    
    driver.get(url)
    time.sleep(3)
    
    #-------cookie accept
    # driver.find_element_by_class_name("button--solid privacy-alert__agree-button").click()
    driver.find_element_by_xpath(" /html/body/div[3]/div[1]/div/div/button[2]").click()    
    time.sleep(2)
    
    #----get the date   calendarbutton-1009-btnInnerEl
    dateLine = driver.find_element_by_id("calendarbutton-1009-btnInnerEl")
    dateStr = dateLine.text     
    destFileFullPath = dir_destFile + '/' + dateStr + ".csv" 

    #-- go to the tab    
    driver.find_element_by_id("notionalvalueSummaryBtn").click()
    time.sleep(2)
    
    # --- expend the table  
    nyse = 'deagg-integrated-nysepnacm'
    driver.find_element_by_id(nyse).click()
    time.sleep(1)
    
    nasdaq = 'deagg-integrated-nasdaqbxq'
    driver.find_element_by_id(nasdaq).click()
    time.sleep(1)
    
    cbeo    = "deagg-integrated-cboezykj"
    driver.find_element_by_id(cbeo).click()
    time.sleep(1)
    
    trf = 'deagg-otc-trfsdqdndb'
    driver.find_element_by_id(trf).click()
    time.sleep(1)
    
    #--get the table
        # ele = driver.find_element_by_class_name("bats-table")
    ele = driver.find_element_by_xpath("/html/body/main/section[1]/div/div[1]/div[4]/table/tbody/tr/td/div/table")
    tbl = ele.get_attribute('outerHTML')
    df  = pd.read_html(tbl)
    df1 = df[0].dropna(how='all')
    driver.quit()
    
    for index1, row in df1.iterrows():
        if "volume" in (row[0]).lower():
            # print(row[index1])
            # print(index1)
            df1 = df1.drop([index1])
    
    df2 = df1.dropna(axis = 1, how='all')    
    df2.insert(0, 'Date', dateStr)
    
    #-------convert money and percentage
    # for (columnName, columnData) in df2.iteritems():
    #     if "$" in columnData[0]:
    #         df2[columnName] = ((df2[columnName].str.strip("$")).str.replace(',','') ).astype(float)
    #         pass
    #     elif "%" in columnData[0]:
    #         df2[columnName] = (df2[columnName].str.strip("%") ).astype(float)/100
    #     else:
    #         pass
    # df = df.replace({np.NAN: None})     
    df2.to_csv(destFileFullPath, index = False) # float_format='%.3f')
    print("Cbeo equity market stat trading value downloaded: " + dateStr)

    df_data = dataframeConvert(destFileFullPath)
    df_data.to_csv(destFileFullPath, index = False, float_format='%.4f')
    
    return destFileFullPath

# url = _url_EquityMarketStat_daily 
# dir_destFile = _dir_EquityMarketStat_daily_TradingValue
# save_EquityMarketStat_daily_TradingValue(url, dir_destFile)



    
    # df = df.replace({np.NAN: None}) 
    # pass
            
# fileFullPath = "G:\\Projects\\HFinvest\\Cboe\\EquityMarketStat_daily\\TradingValue\\2021-10-08.csv"    
# dataframeConvert(fileFullPath)


def Cboe_EquityMarketStat_daily_run():
    url             = _url_EquityMarketStat_daily
    dir_destFile    = _dir_EquityMarketStat_daily_Vol
    
    csvFileFullPath = save_EquityMarketStat_csvFile_daily_Volume(url, dir_destFile)    
    sql_Cboe_EquityMarketStat_csvFile_daily_Volume(csvFileFullPath)

# Cboe_EquityMarketStat_daily_run()



  

   

  
						
