# -*- coding: utf-8 -*-
"""
@author: haoli
"""
import sys
sys.path.append("../")
import const_common as constA
# import downloadUpdateData as mydownPy

import downloadUpdateData as mydownPy


# import requests
from os import makedirs
import os.path as myPath
import pandas as pd

# from urllib.request import urlopen, Request
# from pathlib import Path 
from datetime import datetime

import os

import pyodbc
# import numpy as np

import time
from selenium import webdriver

import ntpath

import pyautogui #, time
pyautogui.PAUSE =2.5

import requests
from bs4 import BeautifulSoup
import re

#----------------------------------
errorFileTargetDir = '../'
# mydownPy.logError("my test message")
#logError(errorFileTargetDir, msg)
# mydownPy.logError(errorFileTargetDir, "my test message")

dir_OptionMarketStat_daily = './OptionMarketStat_daily'

dir_OptionMarketStat_daily_webpage='./OptionMarketStat_daily'
_url_OptionMarketStat_daily = "https://www.cboe.com/us/options/market_statistics/daily/"
_savedName_webpage = "Cboe_OptionMarketStat_daily.html"

# _url_Picture_CNN_Fear_Greed = "http://markets.money.cnn.com/Marketsdata/Api/Chart/FearGreedHistoricalImage?inputOrder=IGHYPtile,VIXPtile,SPXPtile,StkBdPtile,McOscPtile,NHNLPtile,PutCallPtile,AvgPtileModel"

# _savedName_picture = "CNN_Fear_Geed.png"



#--------table name ---------
_sqlTable_OptionMarketStat_daily = 'Cboe_OptionMarketStat_daily'  

import key as pconst
_server = pconst.RYAN_SQL['server']
_username = pconst.RYAN_SQL['username']
_password = pconst.RYAN_SQL['password']  
_database = 'Fear_Greed' 


pd.set_option('mode.chained_assignment', None)




def makeTodayDataDir(newDir):
    # if not myPath.lexists(newDir): #lexists
    if not myPath.exists(newDir):
        makedirs(newDir)

def convert_dateStr(MMMMddyyyy):
    return datetime.strptime(MMMMddyyyy, '%B %d, %Y').strftime('%Y-%m-%d')
        
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


def sql_Cboe_OptionMarketStat_daily_HTML(htmlFileFullPath):
    myDataFrameLists = pd.read_html(htmlFileFullPath)   
    if len(myDataFrameLists) == 0:
        msg = "empty Cbeo option market stat daily table from website: " + htmlFileFullPath
        mydownPy.logError(errorFileTargetDir, msg)  
        return
    else: 
        # htmlFilePath = constA.getFilePathInfo(htmlFileFullPath, 0)
        metalName    = constA.getFilePathInfo(htmlFileFullPath, 2).strip()
        # date_fromFolderName  = constA.getFilePathInfo(htmlFilePath, 1) 
              
        #----------build the dataframe and save it
        df_ClosePrice = (myDataFrameLists[0])
        df_ClosePrice = df_ClosePrice.replace({np.NAN: None})
        df_ClosePrice1 = df_ClosePrice.iloc[1:,:]
        df = convertDDMM_date(df_ClosePrice1, 0)        
        df.insert(1, "name", metalName)
        
        # ----- connect the database        
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server+';DATABASE='+_database+';UID='+_username+';PWD='+_password)
        cursor = cnxn.cursor()  
        
        count =0 
        for (index, data) in df.iterrows(): 
            count += 1
            if count >3:
                break
            params =  tuple(data) 
            date_del = data[0]
            # print (data[0])   
            query = """DELETE FROM %s where Date = '%s' and Name = '%s' ;""" % (_sqlTable_LME_Lithium_ColsePrice2021, date_del, metalName)
            cursor.execute(query)
             
            query = """INSERT INTO %s VALUES (?,?,? );""" %(_sqlTable_LME_Lithium_ColsePrice2021)
            cursor.execute(query, params)
        cnxn.commit()
        
        # -----close database connection ----------
        cursor.close()
        cnxn.close()           
htmlFileFullPath = dir_OptionMarketStat_daily_webpage +'/2021-10-04/Cboe_OptionMarketStat_daily.html'
sql_Cboe_OptionMarketStat_daily_HTML(htmlFileFullPath)
print()






dir_OptionMarketStat_daily = './OptionMarketStat_daily'

dir_OptionMarketStat_daily_webpage='./OptionMarketStat_daily'
_url_OptionMarketStat_daily = "https://www.cboe.com/us/options/market_statistics/daily/"
_savedName_webpage = "Cboe_OptionMarketStat_daily.html"



# def html_Fear_Greed_CNN():    
#     # url = myFINRA._FINRA_MarginStatistics_URL
#     url = 'https://money.cnn.com/data/fear-and-greed/'
#     # url = "G:/Projects/HFinvest/Fear & Greed Index - Investor Sentiment - CNNMoney.html"
 
#     driver = webdriver.Chrome('../chromedriver.exe')
#     driver.get(url)
#     time.sleep(10)    
#     pass


# html_Fear_Greed_CNN()  

def save_Fear_Greed_CNN(list_Date_Val):
    fileDir = dir_Fear_Greed
    makeTodayDataDir(fileDir)
    
    fileFullDir = fileDir + "/Fear_Greed_CNN.csv"
    df = pd.read_csv(fileFullDir)
    df.loc[len(df)] = list_Date_Val
    df.to_csv(fileFullDir, index= False)

# list_Date_Val = [0, 0]
# save_Fear_Greed_CNN(list_Date_Val)
# print()

def webpage_Greed_Fear_CNN(url, dbName):
    r = requests.get(url)
    time.sleep(5)
    soup =   BeautifulSoup(r.content,"lxml")
    # w3schollsList = soup.find_all('ul')
    # ulList = w3schollsList[13].find_all('li')
    # for li in ulList:
    #     print(li)  /html/body/main/section/div/div[1]/div/div/div/button/span[2]
      
    #------get Date---
    dateLine = soup.find_all('div', id = ("needleAsOfDate"))
    # print(dateLine[0].text)
    b = (dateLine[0].text).split('Last updated')
    b1 = b[1].split('at')  
    dateStr = b1[0].strip()     
    dateStr1 = convertDDMM_date(dateStr)
    # print(dateStr1)
    preYearDate = date_1yr_pre(dateStr1)
    
    greedLine = soup.find_all('li', string = re.compile("Greed Now"))
    a1 = (greedLine[0].text).strip().split('Greed Now')
    a = a1[1].strip().split(' ') 
    for g in a:
        try:  
            greedVal = float(g)
            print (dateStr1 + ':  ' + greedLine[0].text)
        except ValueError:
            pass    
        
    # Fear & Greed 1 Year Ago: 41 (Fear)
    greedLine_preYear = soup.find_all('li', string = re.compile("Greed 1 Year Ago"))
    a1 = (greedLine_preYear[0].text).strip().split('Greed 1 Year Ago')
    a = a1[1].strip().split(' ') 
    for g in a:
        try:  
            greedVal_preYear = float(g)
            print (preYearDate + ':  ' + greedLine_preYear[0].text)
        except ValueError:
            pass
    
    #------database --------------------   
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server+';DATABASE='+_database+';UID='+_username+';PWD='+_password)
    cursor = cnxn.cursor()
     
    query = """DELETE FROM %s where Date = '%s' ;""" % (dbName, dateStr1)
    cursor.execute(query)         

    params = tuple([dateStr1, greedVal])
    query = """INSERT INTO %s VALUES (?,? );""" %(dbName)
    cursor.execute(query, params)

    #-------pre year-----
      
    # if "2021-08-24" > preYearDate :        
    #     query = """DELETE FROM %s where Date = '%s' ;""" % (dbName, preYearDate)
    #     cursor.execute(query)         
    
    #     params_pre = tuple([preYearDate, greedVal_preYear])  
    #     query = """INSERT INTO %s VALUES (?,? );""" %(dbName)
    #     cursor.execute(query, params_pre)    
    #     print("Fear_Greed_CNN :  " +   params_pre)
        
    cnxn.commit()        
    cursor.close()
    cnxn.close()
    print ("Fear_Greed_CNN sql updated:  " +   dateStr1)
    
    #----save csv file
    list_Date_Val = [dateStr1, greedVal]
    save_Fear_Greed_CNN(list_Date_Val) 

    list_Date_Val = [preYearDate, greedVal_preYear]
    save_Fear_Greed_CNN(list_Date_Val)  
    
    #-------save webpage----------
    destFilePath =  dir_Fear_Greed_webpage + '/' + dateStr1
    url = _url_CNN_Fear_Greed
    destFileName = _savedName_webpage
    saveWebPage_Fear_Greed_CNN(url, destFilePath, destFileName)
    
    url1 = _url_Picture_CNN_Fear_Greed
    destFileName1 = _savedName_picture    
    saveWebPage_Fear_Greed_CNN(url1, destFilePath, destFileName1)    
# dbName = _sqlTable_Fear_Greed_CNN
# url = _url_CNN_Fear_Greed
# webpage_Greed_Fear_CNN(dbName)


    
def daily_run_CNN_Fear_Greed():
    dbName = _sqlTable_Fear_Greed_CNN
    url = _url_CNN_Fear_Greed
    webpage_Greed_Fear_CNN(url, dbName)
       
       
# daily_run_CNN_Fear_Greed()


def loadcsv_sql(dbName, fileFullPath):    
    df = pd.read_csv(fileFullPath)
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server+';DATABASE='+_database+';UID='+_username+';PWD='+_password)
    cursor = cnxn.cursor()
    
    for row in range (len(df)):        
        query = """DELETE FROM %s where Date = '%s' ;""" % (dbName, df.iat[row, 0])
        cursor.execute(query)
        
        params = tuple([df.iat[row, 0], float(df.iat[row, 1]) ]) 
        query = """INSERT INTO %s VALUES (?,? );""" %(dbName)
        cursor.execute(query, params)   
        
    cnxn.commit()        
    cursor.close()
    cnxn.close()    
# fileFullPath = "G:\\Projects\\HFinvest\\Fear_Greed\\Fear_Greed\\Backup2011-2020\\cnn fear greed 2011-2020_2_missing2020.csv"
# dbName = _sqlTable_Fear_Greed_CNN
# loadcsv_sql(dbName, fileFullPath) 


  
						
