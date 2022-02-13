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


# import requests
# from bs4 import BeautifulSoup
# import re

#----------------------------------
errorFileTargetDir = '../'
# mydownPy.logError("my test message")
#logError(errorFileTargetDir, msg)
# mydownPy.logError(errorFileTargetDir, "my test message")

dir_OptionMarketStat_daily = './OptionMarketStat_daily'

dir_OptionMarketStat_daily_webpage='./OptionMarketStat_daily'
_url_OptionMarketStat_daily = "https://www.cboe.com/us/options/market_statistics/daily/"
_savedName_webpage = "Cboe_OptionMarketStat_daily.html"


#--------table name ---------
_sqlTable_PutCall_ratio_A = 'PutCall_ratio_A'  
_sqlTable_PutCall_ratio_B = 'PutCall_ratio_B'

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
    
    # driver.find_element_by_class_name("button--solid privacy-alert__agree-button").click()
    driver.find_element_by_xpath(" /html/body/div[3]/div[1]/div/div/button[2]").click()
    
    time.sleep(3)
    # /html/body/div[3]/div[1]/div/div/button[2] /html/body/div[3]/div[1]/div/div/button[2]  button--solid privacy-alert__agree-button
    dateLine = driver.find_element_by_xpath("/html/body/main/section/div/div[1]/div/div/div/button/span[2]")
    
    print(dateLine.text)
    dateStr = convert_dateStr((dateLine.text))
    
    destFilePath = dir_destFile + '/' + dateStr    
    
    # -------- make file dir, delete old file and set the file name   
    makeTodayDataDir(destFilePath)
    fileFullPath = destFilePath + '/' + destFileName
    # fileFullPath = destFilePath_2 + '/' + destFileName
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
    # time.sleep(2)
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
def downloadHistory(dir_destFile, destFileName):
    driver = webdriver.Chrome('../chromedriver.exe')
    driver.implicitly_wait(10)  
    
    # date_list = [datetime.strptime('2019-01-02', "%Y-%m-%d") + timedelta(days=x) for x in range(278)]    
    date_list = [datetime.strptime('2021-10-07', "%Y-%m-%d") + timedelta(days=x) for x in range(1)]    
    
    for d in date_list:
        if d.weekday() == 5 or d.weekday() == 6:
            print ("weekend: " +  d.strftime("%Y-%m-%d"))
        else:        
            # print ("?dt=" + d.strftime("%Y-%m-%d"))    
            url = "https://www.cboe.com/us/options/market_statistics/daily/?dt=" + d.strftime("%Y-%m-%d")
            driver.get(url)
            time.sleep(10)            
            # driver.find_element_by_class_name("button--solid privacy-alert__agree-button").click()
            # driver.find_element_by_xpath(" /html/body/div[3]/div[1]/div/div/button[2]").click()
            # time.sleep(3)
            
            # /html/body/div[3]/div[1]/div/div/button[2] /html/body/div[3]/div[1]/div/div/button[2]  button--solid privacy-alert__agree-button
            dateLine = driver.find_element_by_xpath("/html/body/main/section/div/div[1]/div/div/div/button/span[2]")
            
            # print(dateLine.text)
            dateStr = convert_dateStr((dateLine.text))
            
            destFilePath = dir_destFile + '/' + dateStr    
            
            # -------- make file dir, delete old file and set the file name   
            makeTodayDataDir(destFilePath)
            fileFullPath = destFilePath + '/' + destFileName
            # fileFullPath = destFilePath_2 + '/' + destFileName
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

# dir_destFile = dir_OptionMarketStat_daily_webpage
# dir_destFile = "G:\Projects\HFinvest\Cboe\OptionMarketStat_daily"
# destFileName = _savedName_webpage
# downloadHistory(dir_destFile, destFileName)
def sql_Cboe_OptionMarketStat_daily_HTML_putCallRatio_before2012_06(htmlFileFullPath):
    myDataFrameLists = pd.read_html(htmlFileFullPath, attrs={"id": "ContentTop_ctl09_lvMktStatsRatios_tabMktStatsRatios"})   
    if len(myDataFrameLists) == 0:
        msg = "empty Cbeo option market stat daily table from website: " + htmlFileFullPath
        mydownPy.logError(errorFileTargetDir, msg)  
        return
    else: 
        htmlFilePath = constA.getFilePathInfo(htmlFileFullPath, 0)
        # metalName    = constA.getFilePathInfo(htmlFileFullPath, 2).strip()
        date_fromFolderName  = constA.getFilePathInfo(htmlFilePath, 1) 
        # df_ratio = ((myDataFrameLists[0]).iloc[1:6, 2:4]).copy()  
        df_ratio = ((myDataFrameLists[0]).iloc[ [1,2,3,4], [2,3]])
        df_ratio.reset_index()        
        # ----- ration  ---- connect the database        
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server+';DATABASE='+_database+';UID='+_username+';PWD='+_password)
        cursor = cnxn.cursor()  
        
        #----the dataframe change it becomes data[2,3]
        for (index, data) in df_ratio.iterrows(): 
            date_del = date_fromFolderName
            rationName = data[2]             
            query = """DELETE FROM %s where Date = '%s' and Name = '%s' ;""" % (_sqlTable_PutCall_ratio_A, date_del, rationName)
            cursor.execute(query)
            
            params =  tuple([date_fromFolderName, rationName, data[3]])            
            # print (params)
            # print (htmlFileFullPath)            
            query = """INSERT INTO %s VALUES (?,?,? );""" %(_sqlTable_PutCall_ratio_A)
            cursor.execute(query, params)

        cnxn.commit()
        print ("Cbeo putCallRatio sql:  " + date_fromFolderName)        
        # -----close database connection ----------
        cursor.close()
        cnxn.close()    
# htmlFileFullPath = 'G:\\Projects\\HFinvest\\Cboe\\2019\\2019-01-02\\Cboe_OptionMarketStat_daily.html'
# sql_Cboe_OptionMarketStat_daily_HTML_putCallRatio_before2012_06(htmlFileFullPath)
# print()

def sql_Cboe_OptionMarketStat_daily_HTML_putCallRatio(htmlFileFullPath):
    myDataFrameLists = pd.read_html(htmlFileFullPath, attrs={"id": "ContentTop_ctl09_lvMktStatsRatios_tabMktStatsRatios"})   
    if len(myDataFrameLists) == 0:
        msg = "empty Cbeo option market stat daily table from website: " + htmlFileFullPath
        mydownPy.logError(errorFileTargetDir, msg)  
        return
    else: 
        htmlFilePath = constA.getFilePathInfo(htmlFileFullPath, 0)
        # metalName    = constA.getFilePathInfo(htmlFileFullPath, 2).strip()
        date_fromFolderName  = constA.getFilePathInfo(htmlFilePath, 1) 
        # df_ratio = ((myDataFrameLists[0]).iloc[1:6, 2:4]).copy()  
        df_ratio = ((myDataFrameLists[0]).iloc[ [1,2,3,4,5], [2,3]])
        df_ratio.reset_index()        
        # ----- ration  ---- connect the database        
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server+';DATABASE='+_database+';UID='+_username+';PWD='+_password)
        cursor = cnxn.cursor()  
        
        #----the dataframe change it becomes data[2,3]
        for (index, data) in df_ratio.iterrows(): 
            date_del = date_fromFolderName
            rationName = data[2]             
            query = """DELETE FROM %s where Date = '%s' and Name = '%s' ;""" % (_sqlTable_PutCall_ratio_A, date_del, rationName)
            cursor.execute(query)
            
            params =  tuple([date_fromFolderName, rationName, data[3]])            
            # print (params)
            # print (htmlFileFullPath)            
            query = """INSERT INTO %s VALUES (?,?,? );""" %(_sqlTable_PutCall_ratio_A)
            cursor.execute(query, params)

        cnxn.commit()
        print ("Cbeo putCallRatio sql:  " + date_fromFolderName)        
        # -----close database connection ----------
        cursor.close()
        cnxn.close()    
# htmlFileFullPath = 'G:\\Projects\\HFinvest\\Cboe\\2019\\2019-01-02\\Cboe_OptionMarketStat_daily.html'
# sql_Cboe_OptionMarketStat_daily_HTML_putCallRatio(htmlFileFullPath)
# print()


def sql_Cboe_OptionMarketStat_daily_HTML_vol_OpenInterest(htmlFileFullPath):
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
# sql_Cboe_OptionMarketStat_daily_HTML_vol_OpenInterest(htmlFileFullPath)
# print()

def loadAllFiles():
    # sourceDir = "G:\Projects\HFinvest\Cboe\OptionMarketStat_daily"
    # sourceDir = "G:\\Projects\\HFinvest\\Cboe\\2019"
    # sourceDir = "G:\\Projects\\HFinvest\\Cboe\\2018"
    # sourceDir = "G:\\Projects\\HFinvest\\Cboe\\2016"
    sourceDir = "G:\\Projects\\HFinvest\\Cboe\\2012-06-Before"

    # pathlist = Path(sourceDir).glob('**/*.html')
    pathlist = Path(sourceDir).glob('**/Cboe_OptionMarketStat_daily.html')    
    for path in pathlist:
         # because path is object not string
         # print(path)
         htmlFileFullPath = str(path)
         # sql_Cboe_OptionMarketStat_daily_HTML_putCallRatio(htmlFileFullPath)
         sql_Cboe_OptionMarketStat_daily_HTML_putCallRatio_before2012_06(htmlFileFullPath)
          
         # sql_Cboe_OptionMarketStat_daily_HTML_vol_OpenInterest(htmlFileFullPath)    
# loadAllFiles() 


def downloadHistory_2019(dir_destFile, destFileName, date_list):
    driver = webdriver.Chrome('../chromedriver.exe')
    driver.implicitly_wait(10)    
    
    # 2019-01-02
    # date_list = [datetime.strptime('2019-01-21', "%Y-%m-%d") + timedelta(days=x) for x in range(260)]    
    # date_list = [datetime.strptime('2018-01-02', "%Y-%m-%d") + timedelta(days=x) for x in range(364)]    
    # date_list = [datetime.strptime('2016-01-02', "%Y-%m-%d") + timedelta(days=x) for x in range(364)]    
    # date_list = [datetime.strptime('2015-01-02', "%Y-%m-%d") + timedelta(days=x) for x in range(364)]    
    
    print (datetime.now())
    for d in date_list:
        if d.weekday() == 5 or d.weekday() == 6:
            print ("weekend: " +  d.strftime("%Y-%m-%d"))
        else:          
            url = "https://cdn.cboe.com/resources/us/options/market_statistics/daily/cone/archive/html/" + d.strftime("%Y-%m-%d") + ".html"
            driver.get(url)
            time.sleep(5)
            
            # driver.find_element_by_class_name("button--solid privacy-alert__agree-button").click()
            # driver.find_element_by_xpath(" /html/body/div[3]/div[1]/div/div/button[2]").click()
            # time.sleep(3)
            
            # /html/body/div[3]/div[1]/div/div/button[2] /html/body/div[3]/div[1]/div/div/button[2]  button--solid privacy-alert__agree-button
            try:
                dateLine = driver.find_element_by_xpath("/html/body/div/div[2]/div[4]/table[2]/tbody/tr/td/div/table/tbody/tr/td/table/tbody/tr/td/h2/span")
            except NoSuchElementException:
                time.sleep(1)
                continue
                # pass 
            # print(dateLine.text)
            dateStr = convert_dateStr_2019((dateLine.text))
            
            destFilePath = dir_destFile + '/' + dateStr    
            
            # -------- make file dir, delete old file and set the file name   
            makeTodayDataDir(destFilePath)
            fileFullPath = destFilePath + '/' + destFileName
            # fileFullPath = destFilePath_2 + '/' + destFileName
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
                        
            if (d.strftime("%m-%d") == "12-31"):
            # if (d.strftime("%m-%d") == "05-06"):
                break
    driver.quit()        
    print (datetime.now())        
        

def download_perod_ofDays():    
    dir_destFile = "G:\Projects\HFinvest\Cboe\OptionCbeoOnly_history_VolOI_a"
    
    destFileName = _savedName_webpage
    date_list1 = [datetime.strptime('2003-10-28', "%Y-%m-%d") + timedelta(days=x) for x in range(364)]    
    date_list2 = [datetime.strptime('2004-01-02', "%Y-%m-%d") + timedelta(days=x) for x in range(364)]    
    date_list3 = [datetime.strptime('2005-01-02', "%Y-%m-%d") + timedelta(days=x) for x in range(364)]    
    # date_list3 = [datetime.strptime('2009-05-07', "%Y-%m-%d") + timedelta(days=x) for x in range(240)]    

    # date_list9 = [datetime.strptime('2006-01-02', "%Y-%m-%d") + timedelta(days=x) for x in range(364)]    
        
    date_list_a = [date_list1, date_list2, date_list3]
    # date_list_a = [date_list2]
    for dList in range(len(date_list_a)):
        date_list = date_list_a[dList]
        # print(date_list)
        downloadHistory_2019(dir_destFile, destFileName,date_list)    
download_perod_ofDays()
   

  
						
