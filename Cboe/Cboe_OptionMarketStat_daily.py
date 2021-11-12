# -*- coding: utf-8 -*-
"""
@author: haoli
"""
import sys
sys.path.append("../")
import const_common as constA
# import downloadUpdateData as mydownPy

import downloadUpdateData as mydownPy

from datetime import datetime
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

dir_OptionMarketStat_daily          = './OptionMarketStat_daily'
dir_OptionMarketStat_daily_webpage  = './OptionMarketStat_daily'
_url_OptionMarketStat_daily = "https://www.cboe.com/us/options/market_statistics/daily/"
_savedName_webpage = "Cboe_OptionMarketStat_daily.html"


#--------table name ---------
_sqlTable_PutCall_ratio_A = 'PutCall_ratio_A'  
_sqlTable_PutCall_ratio_B = 'PutCall_ratio_B_Vol_OI'

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

def date_1yr_pre(yymmdd_str):
    yy = yymmdd_str.split('-')
    year = int(yy[0]) - 1
    dateStr = str(year) + '-' + yy[1] + '-' + yy[2]
    return dateStr

def saveWebPage_OptionMarketStat_daily(url, dir_destFile, destFileName): 
    driver = webdriver.Chrome('../chromedriver.exe')
    driver.implicitly_wait(10)
    
    driver.get(url)
    time.sleep(3)
    
    #--- agreemnet 
    # driver.find_element_by_class_name("button--solid privacy-alert__agree-button").click()
    # driver.find_element_by_xpath("/html/body/div[3]/div[1]/div/div/button[2]").click()
    driver.find_element_by_xpath("/html/body/div[3]/div[2]/div/div/button").click()
    time.sleep(3)

    
    dateLine = driver.find_element_by_xpath("/html/body/main/section/div/div[1]/div/div/div/button/span[2]")
    # dateLine = driver.find_element_by_id("calendarbutton-1009-btnInnerEl")
    # print(dateLine.text) Button__TextContainer-sc-1tdgwi0-1 hFHkoL
    dateStr = convert_dateStr((dateLine.text))    
    destFilePath = dir_destFile + '/' + dateStr    
    
    # -------- make file dir, delete old file and set the file name   
    makeTodayDataDir(destFilePath)
    fileFullPath = destFilePath + '/' + destFileName
    
    if os.path.isfile(fileFullPath):
        os.remove(fileFullPath)
        print('file removed: ' + fileFullPath)
        time.sleep(5)
        
    #-----convert python dir to windows dir 
    fileAbsPath = os.path.abspath(fileFullPath)   
    winPath = fileAbsPath.replace(os.sep,ntpath.sep)
    
    pyautogui.hotkey('ctrl', 's')
    time.sleep(2)
    
    pyautogui.typewrite(winPath)
    time.sleep(2)
    
    pyautogui.hotkey('enter')
    time.sleep(5) #wait for download finish
    
    driver.quit()    
    time.sleep(1)
    print (" --- Option Market Stat daily webpage saved: " + url)
    #check if the file is download with data
    # fileSize = os.stat(fileFullPath).st_size
    # if fileSize < 1000: 
    #     msg = "website download data <1K: " + fileFullPath + " ; url: " + url 
    #     mydownPy.logError(errorFileTargetDir, msg)
    # else: # save, update the data
    #     print('file donwloaded: ' + url)        
    return fileFullPath 
# url = _url_OptionMarketStat_daily
# dir_destFile = dir_OptionMarketStat_daily_webpage
# destFileName = _savedName_webpage
# saveWebPage_OptionMarketStat_daily(url, dir_destFile, destFileName)
# print() 

def sql_Cboe_OptionMarketStat_daily_HTML_putCallRatio(htmlFileFullPath):
    myDataFrameLists = pd.read_html(htmlFileFullPath)   
    if len(myDataFrameLists) == 0:
        msg = "empty Cbeo option market stat daily table from website: " + htmlFileFullPath
        mydownPy.logError(errorFileTargetDir, msg)  
        return
    else: 
        htmlFilePath = constA.getFilePathInfo(htmlFileFullPath, 0)
        # metalName    = constA.getFilePathInfo(htmlFileFullPath, 2).strip()
        date_fromFolderName  = constA.getFilePathInfo(htmlFilePath, 1) 
        df_ratio = myDataFrameLists[0]          
        # ----- ration  ---- connect the database        
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server+';DATABASE='+_database+';UID='+_username+';PWD='+_password)
        cursor = cnxn.cursor()  
        
        for (index, data) in df_ratio.iterrows(): 
            date_del = date_fromFolderName
            rationName = data[0].strip()             
            query = """DELETE FROM %s where Date = '%s' and Name = '%s' ;""" % (_sqlTable_PutCall_ratio_A, date_del, rationName)
            cursor.execute(query)
            
            params =  tuple([date_fromFolderName, rationName, data[1]])            
            # print (params)
            # print (htmlFileFullPath)            
            query = """INSERT INTO %s VALUES (?,?,? );""" %(_sqlTable_PutCall_ratio_A)
            cursor.execute(query, params)

        cnxn.commit()
        print ("Cbeo putCallRatio sql:  " + date_fromFolderName)        
        # -----close database connection ----------
        cursor.close()
        cnxn.close()    
# htmlFileFullPath = dir_OptionMarketStat_daily_webpage +'/2021-10-04/Cboe_OptionMarketStat_daily.html'
# sql_Cboe_OptionMarketStat_daily_HTML_putCallRatio(htmlFileFullPath)
# print()


def sql_Cboe_OptionMarketStat_daily_HTML_Vol_OpenInterest(htmlFileFullPath):
    myDataFrameLists = pd.read_html(htmlFileFullPath)   
    if len(myDataFrameLists) == 0:
        msg = "empty Cbeo option market stat daily table from website: " + htmlFileFullPath
        mydownPy.logError(errorFileTargetDir, msg)  
        return
    else: 
        htmlFilePath = constA.getFilePathInfo(htmlFileFullPath, 0)
        # metalName    = constA.getFilePathInfo(htmlFileFullPath, 2).strip()
        date_fromFolderName  = constA.getFilePathInfo(htmlFilePath, 1) 

        # ----- ration  ---- connect the database        
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server+';DATABASE='+_database+';UID='+_username+';PWD='+_password)
        cursor = cnxn.cursor() 
        
        #  tables from 1 to last
        for count in range (1, len(myDataFrameLists)): 
            df = myDataFrameLists[count]
            volOIName = df.columns[0]
            params = (date_fromFolderName, volOIName)
            
            count = 0
            for (columnName, columnData) in df.iteritems():
                if count == 0:
                    count +=1
                    continue               
                date_del = date_fromFolderName
                optionType = columnData[0]                
                query = """DELETE FROM %s where Date = '%s' and Name = '%s' and OptionType = '%s';""" % (_sqlTable_PutCall_ratio_B, date_del, volOIName, optionType)
                cursor.execute(query)
                # print (query)
                params1 = tuple(columnData)
                params2 =  params + params1 
                # print (params2 + "  " + htmlFileFullPath)
                query = """INSERT INTO %s VALUES (?,?,?,?,?);""" %(_sqlTable_PutCall_ratio_B)
                cursor.execute(query, params2)
                # print (params2)
        cnxn.commit()
        print ("Cbeo volume openInterest sql:  " + date_fromFolderName)        
        # -----close database connection ----------
        cursor.close()
        cnxn.close()       
# htmlFileFullPath = dir_OptionMarketStat_daily_webpage +'/2021-10-04/Cboe_OptionMarketStat_daily.html'
# sql_Cboe_OptionMarketStat_daily_HTML_Vol_OpenInterest(htmlFileFullPath)
# print()


# def loadAllFiles():
#     sourceDir = "G:\Projects\HFinvest\Cboe\OptionMarketStat_daily"
    
#     # pathlist = Path(sourceDir).glob('**/*.html')
#     pathlist = Path(sourceDir).glob('**/Cboe_OptionMarketStat_daily.html')    
#     for path in pathlist:
#          # because path is object not string
#          htmlFileFullPath = str(path)
#          # sql_Cboe_OptionMarketStat_daily_HTML_putCallRatio(htmlFileFullPath)    
#          sql_Cboe_OptionMarketStat_daily_HTML_Vol_OpenInterest(htmlFileFullPath)    
# # loadAllFiles()    

def Cbeo_OptionMarketStat_daily():
    
    url = _url_OptionMarketStat_daily
    dir_destFile = dir_OptionMarketStat_daily_webpage
    destFileName = _savedName_webpage
    htmlFileFullPath = saveWebPage_OptionMarketStat_daily(url, dir_destFile, destFileName)
    
    #----------database-----
    sql_Cboe_OptionMarketStat_daily_HTML_putCallRatio(htmlFileFullPath)    
    sql_Cboe_OptionMarketStat_daily_HTML_Vol_OpenInterest(htmlFileFullPath)

Cbeo_OptionMarketStat_daily()




  
						
