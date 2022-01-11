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
from selenium.common.exceptions import NoSuchElementException
import ntpath

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

_dir_OptionSummary_daily         = './OptionSummary_ValueVolume_daily/'
_url_OptionMarketStat_daily      = "https://www.cboe.com/us/options/market_statistics/#current"

#--------table name ---------
_sqlTable_Option_USmarkeySummary_daily      = 'Option_USmarket_TradingSummary_ValueVolume_daily'


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

    # if _sum in colName.lower():
    #     return _sqlTable_Option_CboeSum_daily
    # elif _index in colName.lower():
    #     return _sqlTable_Option_CboeIndex_daily    
    # elif _ETP in colName.lower():
    #     return _sqlTable_Option_CboeExchangeTradeProduct_daily    
    # elif _equity in colName.lower():
    #     return _sqlTable_Option_CboeEquity_daily    
    # elif _VIX in colName.lower():
    #     return _sqlTable_Option_CboeVOLATILITYINDEX_daily    
    # elif _SPX in colName.lower():
    #     return _sqlTable_Option_CboeSPX_daily    
    # elif _OEX in colName.lower():
    #     return _sqlTable_Option_CboeOEX_daily    
    # elif _MRUT in colName.lower()  or _RUT in colName.lower():
    #     return _sqlTable_Option_CboeMRUT_daily
    # elif _PCratio in colName.lower():
    #     return _PCratio       
    # else:
    #     return ""

def saveWebPage_Option_USMarket_summary_daily(url, dir_destFile):     
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
    time.sleep(2)
    
    try:   #--- agreemnet 
        driver.find_element_by_xpath("/html/body/div[3]/div[2]/div/div/button").click()
        time.sleep(1)    
    except NoSuchElementException:  #spelling error making this code not work as expected
        pass    

    dateLine = driver.find_element_by_id("calendarbutton-1009-btnInnerEl")
    dateStr = ((dateLine.text).strip())
    if dateStr == "":
        print("error:   No date found.  " + url)
        driver.quit() 
        return "no date" 

    href_field = driver.find_element_by_id("ms_csvHistory").click()   
    # url_file = href_field.get_attribute('href')    
    fileName = dateStr + '_bats_us_options_mkt_share_last30TradingDay.csv' 

    newFilefullPath = os.path.join(dir_destFile, fileName)    
    if os.path.isfile(newFilefullPath):
        os.remove(newFilefullPath)
        print('file removed: ' + newFilefullPath)
    
    #-----convert python dir to windows dir 
    fileAbsPath = os.path.abspath(newFilefullPath)   
    winPath = fileAbsPath.replace(os.sep,ntpath.sep)    
    
    time.sleep(2)
    pyautogui.typewrite(winPath)
    time.sleep(2)    
    pyautogui.hotkey('enter')
    time.sleep(2) #wait for download finish
    driver.quit()
    print('Downloaded Option US market summary:   ' + fileName)  
    return newFilefullPath
# url = _url_OptionMarketStat_daily
# dir_destFile = _dir_OptionSummary_daily
# saveWebPage_Option_USMarket_summary_daily(url, dir_destFile)
# print() 

def sql_daily_USmarket_summary_30days(sourceFileFullpath, dbName, islast10day):    
    df = pd.read_csv(sourceFileFullpath)    
    df = df.replace({np.NAN: None})
    # df[df.columns[1]] = df[df.columns[1]].str.slice(0,60)
    
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server+';DATABASE='+_database+';UID='+_username+';PWD='+_password)
    cursor = cnxn.cursor()
    
    count =0
    for index, row in df.iterrows():
        query = """DELETE FROM %s where Date = '%s' and [Market Participant] = '%s';""" \
                                % (dbName, row[0], row[1])
        cursor.execute(query)         

        params = tuple(row)
        query = """INSERT INTO %s VALUES (?,?,?,?, ?,?,?,?, ?,?,?);""" %(dbName)
        cursor.execute(query, params) 
        if islast10day:
            count+=1
            if count >160:
                break        
    cnxn.commit()        
    cursor.close()
    cnxn.close()
    print("sql insert Option US market summary 30days: "   + sourceFileFullpath)
    
# sourceFileFullpath = _dir_OptionSummary_daily + '2021-12-31_bats_us_options_mkt_share.csv'
# dbName = _sqlTable_Option_USmarkeySummary_daily 
# sql_daily_USmarket_summary_30days(sourceFileFullpath, dbName)   
# print()


def download_perod_ofDays(): 
    # date_list1 = [datetime.strptime('2019-10-07', "%Y-%m-%d") + timedelta(days=x) for x in range(85)]    
    # date_list2 = [datetime.strptime('2020-01-02', "%Y-%m-%d") + timedelta(days=x) for x in range(365)]    
    # date_list2 = [datetime.strptime('2020-08-13', "%Y-%m-%d") + timedelta(days=x) for x in range(141)]    
    # date_list3 = [datetime.strptime('2021-11-16', "%Y-%m-%d") - timedelta(days=x) for x in range(363)]    
    date_list3 = [datetime.strptime('2021-12-16', "%Y-%m-%d") - timedelta(days=x) for x in range(1)]    
    # 2015-11-24
    date_list_a = [date_list3]
    for dList in range(len(date_list_a)):
        date_list = date_list_a[dList]
        # print(date_list)
        for d in date_list:
            # if d.weekday() == 5 or d.weekday() == 6:
            #     print ("weekend: " +  d.strftime("%Y-%m-%d"))
            #     continue
            # if (d.strftime("%d") != "16"): 
            #     continue            
           
            url1 = "https://www.cboe.com/us/options/market_statistics/market/"
            #"https://www.cboe.com/us/options/market_statistics/market/2016-01-08/"
            url2 = d.strftime("%Y-%m-%d")        
            url = url1 + url2            

            dir_destFile = _dir_OptionSummary_daily
            sourceFileFullpath = saveWebPage_Option_USMarket_summary_daily(url, dir_destFile)
            
            # sourceFileFullpath = _dir_OptionSummary_daily + '2021-12-31_bats_us_options_mkt_share.csv'
            dbName = _sqlTable_Option_USmarkeySummary_daily 
            islast10day = False
            sql_daily_USmarket_summary_30days(sourceFileFullpath, dbName, islast10day) 
            
            print ("download:  " + d.strftime("%Y-%m-%d"))
            
            # dir_destFile = _dir_OptionSummary_daily
            # msg = saveWebPage_Option_USMarket_summary_daily(url, dir_destFile)
            # if msg == "True":
            #     print ("download:  " + d.strftime("%Y-%m-%d"))
            # else:
            #     print ("------" + d.strftime("%Y-%m-%d")) 
                
            # if (d.strftime("%m-%d") == "12-31"):
            # # if (d.strftime("%m-%d") == "05-06"):
            #     break
# download_perod_ofDays()


def Cbeo_OptionMarketStat_CboeOnly_daily():    
    url = _url_OptionMarketStat_daily
    dir_destFile = _dir_OptionSummary_daily
    sourceFileFullpath = saveWebPage_Option_USMarket_summary_daily(url, dir_destFile)
    
    # sourceFileFullpath = _dir_OptionSummary_daily + '2021-12-31_bats_us_options_mkt_share.csv'
    dbName = _sqlTable_Option_USmarkeySummary_daily 
    islast10day = True
    sql_daily_USmarket_summary_30days(sourceFileFullpath, dbName, islast10day)   


Cbeo_OptionMarketStat_CboeOnly_daily()




  
						
