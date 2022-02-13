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

_OptionCbeoOnly_mostActive_daily          = './OptionCbeoOnly_mostActive_daily/'

_url_OptionCbeoOnly_mostActive_daily = "https://www.cboe.com/us/options/market_statistics/most_active/"


#--------table name ---------
_sqlTable_Option_Cboe_MostActiveVolume_daily     = 'Option_Cboe_MostActiveVolume_daily'




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
    try:  #Jan 7, 22
        return datetime.strptime(MMMMddyyyy, '%b %d, %y').strftime('%Y-%m-%d')
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

def saveWebPage_OptionCboeOnly_daily(url, dir_destFile): 
    driver = webdriver.Chrome('../chromedriver.exe')
    driver.implicitly_wait(10)    
    driver.get(url)
    time.sleep(2)

    #--- agreemnet   /html/body/div[3]/div[1]/div/div/button[2]
    # driver.find_element_by_xpath("/html/body/div[3]/div[2]/div/div/button").click()
    driver.find_element_by_xpath("//html/body/div[3]/div[1]/div/div/button[2]").click()
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
    if (tables[0]).isnull().all().all():
        print ("error no data in table: " + url)
        driver.quit() 
        return ""
    if (len(tables) == 0) :
        print ("error: No Table found.  " + url)
        driver.quit() 
        return ""
    # check the date   /html/body/main/section/div/div/div/div[4]
    dateLine = driver.find_element_by_xpath("/html/body/main/section/div/div/div/div[4]")
    # print(dateLine.text)
    d = dateLine.text.split(",")
    todayStr = "Data for " + (datetime.today().strftime("%b %d")).replace(" 0", " ")
    
    if todayStr.lower() in d[0].lower(): #Data for Jan 6
        pass
    else:
        print ("error: No data for today. Today is " + todayStr.lower() + "   -  website date is: " + d[0].lower() )
        driver.quit()
        return ""
        
    driver.quit()    
    # time.sleep(1)

    dateStr = datetime.today().strftime('%Y-%m-%d')
    dateTimeStrFile = datetime.today().strftime('%Y-%m-%d_%H_%M_%S')
    destFilePath = dir_destFile + '/' +  dateStr   
    makeTodayDataDir(destFilePath)  
    fileFullPath = destFilePath + '/' + "option_mostActive_" + dateTimeStrFile  + ".csv"
        
    if os.path.isfile(fileFullPath):
        os.remove(fileFullPath)
        print('file removed: ' + fileFullPath)
        time.sleep(1)    
    
    dfCall_all = tables[0]
    dfPut_all = tables[1]
    dfCall_index = tables[2]
    dfPut_index = tables[3]
    dfCall_equity = tables[4]
    dfPut_equity = tables[5]    
    
    dfPut_all.insert(0,"Put/Call","put")
    dfPut_index.insert(0,"Put/Call","put")
    dfPut_equity.insert(0,"Put/Call","put")
    
    dfCall_all.insert(0,"Put/Call","call")
    dfCall_index.insert(0,"Put/Call","call")
    dfCall_equity.insert(0,"Put/Call","call")


    df_all = dfPut_all.append(dfCall_all, ignore_index=True)
    df_all.insert(0,'Type',"All")
    
    df_index = dfPut_index.append(dfCall_index, ignore_index=True)
    df_index.insert(0,'Type',"Index")
    
    df_equity = dfPut_equity.append(dfCall_equity, ignore_index=True)
    df_equity.insert(0,'Type',"Equity")
    
    df = df_all.append(df_index, ignore_index=True).append(df_equity, ignore_index=True)
    
    dateTimeStr = datetime.now().strftime('%Y-%m-%d %H:%M:%S') #1955-12-13 12:43:00
    # dateTimeStr = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    df.insert(0,'DateTime',dateTimeStr)

    for i in range(len(df)):
        df.iat[i, 4] = convert_dateStr(str(df.iat[i, 4]))
        # print(df.iat[i, 4])
    df.to_csv(fileFullPath, index=False)      # print(databaseName)        
    print (" --- Option CBOE most active trade saved: " + fileFullPath)
    return fileFullPath
# url = _url_OptionCbeoOnly_mostActive_daily
# dir_destFile = _OptionCbeoOnly_mostActive_daily
# csvFileFullPath = saveWebPage_OptionCboeOnly_daily(url, dir_destFile)
# print() 

    

def sql_CboeOption_mostActive_daily(csvFileFullPath, databaseName):
    df = pd.read_csv(csvFileFullPath)
    df = df.replace({np.NAN: None}) 
    if len(df) == 0:
        print ( "error: most active cbeo option daily: " + csvFileFullPath) 
        return    
    else:         
        # ----- ration  ---- connect the database        
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server+';DATABASE='+_database+';UID='+_username+';PWD='+_password)
        cursor = cnxn.cursor()

        date_del = df.iat[0,0]                   
        query = """DELETE FROM %s where DateTime = '%s' ;""" % (databaseName, date_del)
        cursor.execute(query)
            
        for (index, data) in df.iterrows(): 
            if data[1] == "All":
                continue
            params =  tuple(data)           
            query = """INSERT INTO %s VALUES (?,?,?,?,?, ?,? );""" %(databaseName)
            cursor.execute(query, params)
 
        cnxn.commit()
        print ("Cbeo option most active trading Volume sql:  " + csvFileFullPath)  
        # -----close database connection ----------
        cursor.close()
        cnxn.close()
# csvFileFullPath = _OptionCbeoOnly_mostActive_daily + "2022-01-10/option_mostActive_2022-01-10_16_20_31.csv"
# databaseName = _sqlTable_Option_Cboe_MostActiveVolume_daily
# sql_CboeOption_mostActive_daily(csvFileFullPath, databaseName)
# print() 


def Cbeo_Option_CbeoMostActiveVolume_daily():    
    url = _url_OptionCbeoOnly_mostActive_daily
    dir_destFile = _OptionCbeoOnly_mostActive_daily
    csvFileFullPath = saveWebPage_OptionCboeOnly_daily(url, dir_destFile)
    # csvFileFullPath = _OptionCbeoOnly_mostActive_daily + "2022-01-07/option_mostActive_13_30_27.csv"
    if csvFileFullPath == '':
        return
    
    databaseName = _sqlTable_Option_Cboe_MostActiveVolume_daily
    sql_CboeOption_mostActive_daily(csvFileFullPath, databaseName)

# Cbeo_Option_CbeoMostActiveVolume_daily()

if datetime.today().weekday() ==5 or datetime.today().weekday() == 6:
    pass
else:
    Cbeo_Option_CbeoMostActiveVolume_daily()
    pass



def sql_CboeOption_mostActive_daily_deleteDateTime(databaseName, dateTimeStr):
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server+';DATABASE='+_database+';UID='+_username+';PWD='+_password)
    cursor = cnxn.cursor()

    date_del = dateTimeStr                   
    query = """DELETE FROM %s where DateTime = '%s' ;""" % (databaseName, date_del)
    cursor.execute(query)    
    cnxn.commit()
    cursor.close()
    cnxn.close()

def sql_CboeOption_mostActive_daily_deleteDateTime_File(csvFileFullPath, databaseName):
    df = pd.read_csv(csvFileFullPath) 
    dateTimeStr = df.iat[0,0]
    sql_CboeOption_mostActive_daily_deleteDateTime(databaseName, dateTimeStr)
    
# csvFileFullPath = _OptionCbeoOnly_mostActive_daily + "2022-01-07/option_mostActive_13_30_27.csv"
# databaseName = _sqlTable_Option_Cboe_MostActiveVolume_daily
# sql_CboeOption_mostActive_daily_deleteDateTime_File(csvFileFullPath, databaseName)
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
            # dir_destFile = dir_Option_CbeoOnly_daily
            # msg = saveWebPage_OptionCboeOnly_daily(url, dir_destFile)
            # if msg == "True":
            #     print ("download:  " + d.strftime("%Y-%m-%d"))
            # else:
            #     print ("------" + d.strftime("%Y-%m-%d"))   
						
