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


from dateutil.rrule import rrule, MONTHLY

from dateutil.rrule import rrule, MONTHLY
from datetime import datetime



_dir_EquityMarketStat_daily_TradingValue    = './EquityMarketStat_daily\\TradingValue'



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

# def date_1yr_pre(yymmdd_str):
#     yy = yymmdd_str.split('-')
#     year = int(yy[0]) - 1
#     dateStr = str(year) + '-' + yy[1] + '-' + yy[2]
#     return dateStr


def dataframeConvert(fileFullPath):
    df = pd.read_csv(fileFullPath)        
    for (columnName, columnData) in df.iteritems():
        # if df[df.columns(columnName)].isnull():
        #     continue        
        if "$" in columnData[0]:
            df[columnName] = (df[columnName].str.strip("$").str.replace(',','') )
            df[columnName] = (df[columnName].str.strip("$").str.replace(',','') ).astype(float)
            pass
        elif "%" in columnData[0]:
            df[columnName] = (df[columnName].str.strip("%") ).astype(float)/100
        else:
            pass
    return df
# fileFullPath = "G:\\Projects\\HFinvest\\Cboe\\EquityMarketStat_daily\\TradingValue\\2018-01-15.csv"
# dataframeConvert(fileFullPath)

def downloadHistory_TradingValue(dir_destFile):
    driver = webdriver.Chrome('../chromedriver.exe')
    driver.implicitly_wait(10)    
    
    
    # date_list1 = [datetime.strptime('2015-12-17', "%Y-%m-%d") + timedelta(days=x) for x in range(15)]    
    # date_list2 = [datetime.strptime('2016-04-26', "%Y-%m-%d") + timedelta(days=x) for x in range(250)]    
    # date_list3 = [datetime.strptime('2017-01-02', "%Y-%m-%d") + timedelta(days=x) for x in range(364)]

    # date_list4 = [datetime.strptime('2018-01-16', "%Y-%m-%d") + timedelta(days=x) for x in range(353)]    
    # date_list5 = [datetime.strptime('2019-01-02', "%Y-%m-%d") + timedelta(days=x) for x in range(364)]    
    # date_list6 = [datetime.strptime('2020-11-28', "%Y-%m-%d") + timedelta(days=x) for x in range(35)]
    date_list7 = [datetime.strptime('2021-05-11', "%Y-%m-%d") + timedelta(days=x) for x in range(190)]    
    
    
    # date_list_a = [date_list2]
    date_list_a = [date_list7 ]
    
    print (datetime.now())    
    driver.get("https://www.cboe.com/us/equities/market_statistics/market/2021-09-07/")
    time.sleep(3)
    #-------cookie accept
    # driver.find_element_by_class_name("button--solid privacy-alert__agree-button").click()
    driver.find_element_by_xpath(" /html/body/div[3]/div[1]/div/div/button[2]").click()    
    time.sleep(2)
    
    
    #-----------start looping
    
    for dList in range(len(date_list_a)):
        date_list = date_list_a[dList]    
        for d in date_list:
            if d.weekday() == 5 or d.weekday() == 6:
                print ("weekend: " +  d.strftime("%Y-%m-%d"))
            else:          
                # url = "https://cdn.cboe.com/resources/us/options/market_statistics/daily/cone/archive/html/" + d.strftime("%Y-%m-%d") + ".html"
                url = "https://www.cboe.com/us/equities/market_statistics/market/" + d.strftime("%Y-%m-%d")
                driver.get(url)
                time.sleep(10)                

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
                time.sleep(2)
                
                nasdaq = 'deagg-integrated-nasdaqbxq'
                driver.find_element_by_id(nasdaq).click()
                time.sleep(2)
                
                cbeo    = "deagg-integrated-cboezykj"
                driver.find_element_by_id(cbeo).click()
                time.sleep(2)
                
                trf = 'deagg-otc-trfsdqdndb'
                driver.find_element_by_id(trf).click()
                time.sleep(2)
                
                #--get the table
                    # ele = driver.find_element_by_class_name("bats-table")
                ele = driver.find_element_by_xpath("/html/body/main/section[1]/div/div[1]/div[4]/table/tbody/tr/td/div/table")
                tbl = ele.get_attribute('outerHTML')
                df  = pd.read_html(tbl)
                df1 = df[0].dropna(how='all')
                
                
                for index1, row in df1.iterrows():
                    if "volume" in (row[0]).lower():
                        # print(row[index1])
                        # print(index1)
                        df1 = df1.drop([index1])
                
                df2 = df1.dropna(axis = 1, how='all')    
                df2.insert(0, 'Date', dateStr)

                df2.to_csv(destFileFullPath, index = False) # float_format='%.3f')
                print("Cbeo equity market stat trading value downloaded: " + dateStr)
                
                #convert to correct datatype
                # df_data = dataframeConvert(destFileFullPath)
                # df_data.to_csv(destFileFullPath, index = False, float_format='%.4f')
    driver.quit()
        
dir_destFile = _dir_EquityMarketStat_daily_TradingValue
downloadHistory_TradingValue(dir_destFile) 
print (datetime.now())
print("")



def download_perod_ofDays():    
    dir_destFile = "G:\Projects\HFinvest\Cboe\OptionMarketStat_daily_a"
    destFileName = _savedName_webpage
    date_list1 = [datetime.strptime('2007-01-02', "%Y-%m-%d") + timedelta(days=x) for x in range(364)]    
    date_list2 = [datetime.strptime('2008-01-02', "%Y-%m-%d") + timedelta(days=x) for x in range(364)]    
    date_list3 = [datetime.strptime('2009-01-02', "%Y-%m-%d") + timedelta(days=x) for x in range(364)]    

    date_list9 = [datetime.strptime('2006-01-02', "%Y-%m-%d") + timedelta(days=x) for x in range(364)]    
        
    
    # date_list1 = [datetime.strptime('2010-01-02', "%Y-%m-%d") + timedelta(days=x) for x in range(364)]    
    # date_list2 = [datetime.strptime('2011-01-02', "%Y-%m-%d") + timedelta(days=x) for x in range(364)]    
    # date_list3 = [datetime.strptime('2012-01-02', "%Y-%m-%d") + timedelta(days=x) for x in range(364)]    
    # date_list4 = [datetime.strptime('2013-01-02', "%Y-%m-%d") + timedelta(days=x) for x in range(364)]    
    # date_list5 = [datetime.strptime('2014-01-02', "%Y-%m-%d") + timedelta(days=x) for x in range(364)]    
    # # date_list6 = [datetime.strptime('2014-01-02', "%Y-%m-%d") + timedelta(days=x) for x in range(364)]    
    
    date_list_a = [date_list9, date_list1, date_list2,date_list3]
    for dList in range(len(date_list_a)):
        date_list = date_list_a[dList]
        # print(date_list)
        downloadHistory_2019(dir_destFile, destFileName,date_list)  
        
        
# download_perod_ofDays()






def downloadHistory_vol(dir_destFile):    
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
    
    start = datetime(2010, 2, 1)
    end = datetime(2021, 10, 1)       
    month_list = [d.strftime('%Y-%m-%d') for d in rrule(MONTHLY, dtstart=start, until=end)]

    url = "https://www.cboe.com/us/equities/market_statistics/market/" + "2021-02-01"
    # print (url)
    driver.get(url)
    time.sleep(5)  
    # driver.find_element_by_class_name("button--solid privacy-alert__agree-button").click()  
    driver.find_element_by_xpath("/html/body/div[3]/div[1]/div/div/button[2]").click()
    time.sleep(2)
        
    for d in month_list:   
        url = "https://www.cboe.com/us/equities/market_statistics/market/" + d
        # print (url)
        driver.get(url)
        time.sleep(5)  
        # driver.find_element_by_class_name("button--solid privacy-alert__agree-button").click()  
        # driver.find_element_by_xpath("/html/body/div[3]/div[1]/div/div/button[2]").click()
        # time.sleep(2)
        
        
        #---- download last 30 days
        driver.find_element_by_id("ms_csvHistory").click()
        time.sleep(3)
        
        # destFilePath = dir_destFile + '/' + dateStr    
        
        # # -------- make file dir, delete old file and set the file name   
        # makeTodayDataDir(destFilePath)
        fileFullPath = dir_destFile + '/' + d
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
        time.sleep(3) #wait for download finish
        print (d)    
    driver.quit() 

# dir_destFile = "G:\\Projects\\HFinvest\\Cboe\\EquityMarketStat_daily\\Volume"
# downloadHistory_vol(dir_destFile)




def loadAllFiles():
    # sourceDir = "G:\Projects\HFinvest\Cboe\OptionMarketStat_daily"
    # sourceDir = "G:\\Projects\\HFinvest\\Cboe\\2019"
    # sourceDir = "G:\\Projects\\HFinvest\\Cboe\\2018"
    sourceDir = "G:\\Projects\\HFinvest\\Cboe\\2017"
    # pathlist = Path(sourceDir).glob('**/*.html')
    pathlist = Path(sourceDir).glob('**/Cboe_OptionMarketStat_daily.html')    
    for path in pathlist:
         # because path is object not string
         # print(path)
         htmlFileFullPath = str(path)
         sql_Cboe_OptionMarketStat_daily_HTML_putCallRatio(htmlFileFullPath)
          
         # sql_Cboe_OptionMarketStat_daily_HTML_vol_OpenInterest(htmlFileFullPath)    
# loadAllFiles() 
# 

def downloadHistory_2019(dir_destFile, destFileName):
    driver = webdriver.Chrome('../chromedriver.exe')
    driver.implicitly_wait(10)    
    
    # 2019-01-02
    # date_list = [datetime.strptime('2019-01-21', "%Y-%m-%d") + timedelta(days=x) for x in range(260)]    
    # date_list = [datetime.strptime('2018-01-02', "%Y-%m-%d") + timedelta(days=x) for x in range(364)]    
    date_list = [datetime.strptime('2016-01-02', "%Y-%m-%d") + timedelta(days=x) for x in range(364)]    
    
    print (datetime.now())
    for d in date_list:
        if d.weekday() == 5 or d.weekday() == 6:
            print ("weekend: " +  d.strftime("%Y-%m-%d"))
        else:          
            url = "https://cdn.cboe.com/resources/us/options/market_statistics/daily/cone/archive/html/" + d.strftime("%Y-%m-%d") + ".html"
            driver.get(url)
            time.sleep(10)
            
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
    print (datetime.now())        
    driver.quit()    

# dir_destFile = "G:\Projects\HFinvest\Cboe\OptionMarketStat_daily_a"
# destFileName = _savedName_webpage
# downloadHistory_2019(dir_destFile, destFileName)    

   

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
        df_ratio = ((myDataFrameLists[0]).iloc[ [1,2,3,4,5], [2,3]]).copy() 
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


# def sql_Cboe_OptionMarketStat_daily_HTML_vol_OpenInterest(htmlFileFullPath):
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

						
