# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 13:15:30 2021

http://www.kitconet.com/

@author: haoli

"""

import sys
sys.path.append("../")

import const_common as constA
import downloadUpdateData as mydownPy


import Const_LME_A as constLME_a


# import requests
from os import makedirs
import os.path as myPath
import os

import pandas as pd

# from urllib.request import urlopen, Request

import pyautogui, time
#Set up a 2.5 second pause after each PyAutoGUI call:
pyautogui.PAUSE = 2.5

from selenium import webdriver
from datetime import datetime
import ntpath

from pathlib import Path

import pyodbc
import numpy as np

from urllib.request import urlopen, Request


#----------------------------------
errorFileTargetDir = '../'

_dateSearchBy_ClassName_nonFerrous_gold_silver = "delayed-date.left"
_dateSearchKeyword = "Data valid for"
_waitTime_loadWebsite_LME = 3

_columnName_goldSilver = ['Date', 'Volume', 'Open Interest']

_server = 'RyanPC'
_database = 'Commodity_A1' 
_username = 'hl' 
_password = '123'     

_sqlTable_LME_baseMetal_stock = 'LME_baseMetal_stock'
_sqlTable_LME_baseMetal_price = 'LME_baseMetal_price'
_sqlTable_LME_precious_price = 'LME_precious_price'
_sqlTable_LME_precious_VolOpenInterest = 'LME_precious_VolOpenInterest'

_sqlTable_LME_TraderReport_CA = 'LME_weeklyTraderReport_CA'
_sqlTable_LME_TraderReport_AL = 'LME_weeklyTraderReport_AL'
_sqlTable_LME_TraderReport_gold = 'LME_weeklyTraderReport_Gold'
_sqlTable_LME_TraderReport_silver = 'LME_weeklyTraderReport_Silver'
#------- ---------

# mydownPy.logError("my test message")
#logError(errorFileTargetDir, msg)
# mydownPy.logError(errorFileTargetDir, "my test message")

def makeTodayDataDir(newDir):
    # if not myPath.lexists(newDir): #lexists
    if not myPath.exists(newDir):
        makedirs(newDir)

def getDate_traderReport(dateStr): 
    d = dateStr.strip()
    try: # DD-MM-YYYY        
        date_fromFile = datetime.strptime(d, '%Y-%m-%d')
        return date_fromFile.strftime('%Y-%m-%d')
    except ValueError:
        return "na"        

#--------------------------------------
def sql_traderReport_CA(df, dbName): 
    # --- SQL ----
    df = df.replace({np.NAN: None})
    df[df.columns[1]] = df[df.columns[1]].str.slice(0,39)
    
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server+';DATABASE='+_database+';UID='+_username+';PWD='+_password)
    cursor = cnxn.cursor()
    
    for index, row in df.iterrows():
        dateStr = row[0]
        agentStr = row[1] 
        positionStr  = row[2]       
        query = """DELETE FROM %s where Date = '%s' and [Agent] = '%s' and [Position] = '%s' ;""" % (dbName, dateStr, agentStr, positionStr)
        cursor.execute(query)         

        params = tuple(row)
        query = """INSERT INTO %s VALUES (?,?,?,?, ?,? );""" %(dbName)
        cursor.execute(query, params)        
    cnxn.commit()        
    cursor.close()
    cnxn.close()  
    
    
def extractReport_sql_CA(fileFullPath, dbName):
    df = pd.read_excel(fileFullPath)  
    
    #------get the file date
    dateCol = df[df.columns[0]]
    dateStr = "na"    
    for c in dateCol:
        dateStr = getDate_traderReport(c)
        if not (dateStr == "na") :
            break
    if dateStr == "na" :
        msg = "LME trader report date is not available: " + fileFullPath
        print(msg)
        mydownPy.logError(errorFileTargetDir, msg)
        return
    print (dateStr)
    
    #----find the row contains all long and short cells    
    for index, row in df.iterrows():        
        boolseries = row.str.contains(r'long|short', case = False, na= False)
        if boolseries.sum() >=6 :
            rowNum = index
            # print (row)
            # print (boolseries)
            break    
        
    df_row = df.iloc[rowNum-1 : rowNum+4] # 1 row before and 3 rows after long row   
    # get the columns  #'Risk Reducing directly related to commercial activities' 'Other' 'Total'
    df_col = df_row[df_row.columns[(boolseries)]] 
    df_data = df_col.T
    df_data[df_data.columns[0]].fillna(method = 'ffill', inplace = True)
    df_data.columns = ['Agent', 'Position', 'RiskReducing', 'Other', 'Total']
    df_data.insert(loc=0,column = 'Date', value = dateStr)
    
    # --- save csv data 
    filePath = constA.getFilePathInfo(fileFullPath, 0)
    fileFullPath_new = filePath + '/' + dateStr + '.csv'
    df_data.to_csv(fileFullPath_new, index = False)
    
    #--------sql--------
    df = df_data
    dateStr = dateStr
    sql_traderReport_CA(df, dbName)   
    

# fileFullPath = constLME_a.trderReport_CADir +'/Commitments of Traders Report - CA - 23 April 2021.xls'
# dbName = _sqlTable_LME_TraderReport_CA
# extractReport_sql_CA(fileFullPath, dbName)


def downloadExcelFile(targetDir, fileName, url):
    # makeTodayDataDir(targetDir)     
    newFilefullPath = targetDir + '/' + fileName
    if os.path.isfile(newFilefullPath): 
        print ("Trader Report file exist: " + newFilefullPath)
        return "na" # file exist do nothing
    # os.remove(newFilefullPath)
    # print('file removed: ' + newFilefullPath)    
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3"}
    req = Request(url = url, headers = headers) 
    html = urlopen(req).read()  
    with open(newFilefullPath, 'wb') as outfile:
        outfile.write(html)
    
    fileSize = os.stat(newFilefullPath).st_size    
    if fileSize < 1000: # 1k
        msg = "Excel file download data <1K: " + newFilefullPath + " ; url: " + url 
        mydownPy.logError(errorFileTargetDir, msg)
    else: # save, update the data
        print('Downloaded weekly trader report: ' + newFilefullPath) 
        
    # r = requests.get(url, allow_redirects=True)
    # with open(newFilefullPath, 'wb') as output:
    #     output.write(r.content)    
    # # open('test5.xls', 'wb').write(r.content)    
    # # f = open(newFilefullPath, 'wb')  
    # # f.write(r.content)
    # # f.close()         
    return newFilefullPath 

# url = 'https://www.lme.com/-/media/Files/Market-data/Daily-volumes/2021/04/Daily-volumes-22042021.xlsx'    
# targetDir = constLME_a.commodityLME_dailyVolumeDir
# fileName = 'Daily-volumes-22042021.xlsx'
# downloadExcelFile(targetDir, fileName, url)
# print()

def download_href_traderReport_weekly(url, targetDir):
    driver = webdriver.Chrome('../chromedriver.exe')
    driver.get(url)
    time.sleep(2)    
    
    list_fullPath = []
    for i in range(60):
        elems = driver.find_elements_by_tag_name('a')
        time.sleep(1)
        count_First10File = 0    
        for elem in elems:
            href = elem.get_attribute('href')
            # time.sleep(1)
            # str_Inhref = 'StockBreakdownReportPaging'
            str_InText = 'daily volume'
            if str_InText in (elem.text).lower(): # if str_Inhref in href: # is not None: 
                count_First10File +=1
                # print(href)
                d1 = (elem.text).split('(')
                d2 = d1[0].split('.')
                fileName = d2[0].strip() + '.xlsx'
                # print (fileName) 
                url_excel = href
                
                excelFileFullPath = downloadExcelFile(targetDir, fileName, url_excel)
                if excelFileFullPath == "na":
                    pass
                else:
                    list_fullPath.append(excelFileFullPath)
                    
                print (excelFileFullPath)    
                # print(href)   
            #processed the first 10 excel files     
            
            # if count_First10File >9:
            #     # break   
            #     print('not the href')
        # time.sleep(0.1)
        
        # for elem in elems:
            
        #-----click the next button
        d = driver.find_elements_by_class_name('icon-chevron-right')
        # d = driver.find_elements_by_class_name('next ')  # return a list
        # time.sleep(1)
        # d = driver.find_elements_by_class_name('icon-chevron-right')
        # print (d)
        d[0].click()
        time.sleep(2)
        # print ( (driver.find_elements_by_class_name('next ')).text )
        print()
    
        # <li class="next "><a class="icon-chevron-right" href="#"><span class="accessible">Next</span></a></li>
    driver.quit()    
    time.sleep(1)
    return list_fullPath


url = 'https://www.lme.com/LME-Clear/Technology/Reports/Volumes'  
# url = constLME_a.commodityLME_dailyVolumeDir
targetDir = constLME_a.commodityLME_dailyVolumeDir
list_fullPath = download_href_traderReport_weekly(url, targetDir)
print (list_fullPath)




#----------------------------------------------------------------


def Workingbackup_download_href_traderReport_weekly(url, targetDir):
    driver = webdriver.Chrome('../chromedriver.exe')
    driver.get(url)
    time.sleep(2)    
    
    list_fullPath = []
    while True:
        elems = driver.find_elements_by_tag_name('a')
        count_First10File = 0    
        for elem in elems:
            href = elem.get_attribute('href')
            # str_Inhref = 'StockBreakdownReportPaging'
            str_InText = 'daily volume'
            if str_InText in (elem.text).lower(): # if str_Inhref in href: # is not None: 
                count_First10File +=1
                print(href)
                d1 = (elem.text).split('(')
                d2 = d1[0].split('.')
                fileName = d2[0].strip() + '.xlsx'
                # print (fileName) 
                url_excel = href
                
                excelFileFullPath = downloadExcelFile(targetDir, fileName, url_excel)
                if excelFileFullPath == "na":
                    pass
                else:
                    list_fullPath.append(excelFileFullPath)
                    
                print (excelFileFullPath)    
                # print(href)   
            #processed the first 10 excel files     
            if count_First10File >9:
                break   
                # print('not the href')
    driver.quit()    
    time.sleep(1)
    return list_fullPath












def extract_allExcelFileSubFolders_toSql(sourceDir, dbName):
    # pathlist = Path(sourceDir).glob('**/*.*')
    # pathlist = Path(sourceDir).glob('**/*.xlsx')
    pathlist = Path(sourceDir).glob('**/*.xls')
    for path in pathlist:
         # because path is object not string
         excelFileFullPath = str(path)
         extractReport_sql_CA(excelFileFullPath, dbName)
         
# sourceDir = constLME_a.trderReport_CADir
# dbName = _sqlTable_LME_TraderReport_CA
# sourceDir = constLME_a.trderReport_ALDir
# dbName = _sqlTable_LME_TraderReport_AL
# sourceDir = constLME_a.trderReport_goldDir
# dbName = _sqlTable_LME_TraderReport_gold
# sourceDir = constLME_a.trderReport_silverDir
# dbName = _sqlTable_LME_TraderReport_silver
# extract_allExcelFileSubFolders_toSql(sourceDir, dbName)
    
def weekly_traderReport_CA():
    # url = 'https://www.lme.com/en-GB/Market-Data/Reports-and-data/Commitments-of-traders/Copper' 
    url = constLME_a.CATraderReport_url
    targetDir = constLME_a.trderReport_CADir
    dbName = _sqlTable_LME_TraderReport_CA
    
    #------do not change from here-----
    list_fileFullPath = download_href_traderReport_weekly(url, targetDir)
    # print (list_fullPath)    
    #-----extract and sql----------
    for i in range(len(list_fileFullPath)):
        fileFullPath = list_fileFullPath[i]
        extractReport_sql_CA(fileFullPath, dbName)        
# weekly_traderReport_CA()

def weekly_traderReport_AL():
    url = constLME_a.ALTraderReport_url
    targetDir = constLME_a.trderReport_ALDir
    dbName = _sqlTable_LME_TraderReport_AL
    
    #------do not change from here-----
    list_fileFullPath = download_href_traderReport_weekly(url, targetDir)
    # print (list_fullPath)  
    # #-----extract and sql----------
    for i in range(len(list_fileFullPath)):
        fileFullPath = list_fileFullPath[i]
        extractReport_sql_CA(fileFullPath, dbName)   
# weekly_traderReport_AL()

def weekly_traderReport_gold():
    url = constLME_a.goldTraderReport_url
    targetDir = constLME_a.trderReport_goldDir
    dbName = _sqlTable_LME_TraderReport_gold
    
    #------do not change from here-----
    
    list_fileFullPath = download_href_traderReport_weekly(url, targetDir)
    # print (list_fullPath)  
    # #-----extract and sql----------
    for i in range(len(list_fileFullPath)):
        fileFullPath = list_fileFullPath[i]
        extractReport_sql_CA(fileFullPath, dbName)   
# weekly_traderReport_gold()

def weekly_traderReport_silver():
    url = constLME_a.silverTraderReport_url
    targetDir = constLME_a.trderReport_silverDir
    dbName = _sqlTable_LME_TraderReport_silver
    
    #------do not change from here-----
    
    list_fileFullPath = download_href_traderReport_weekly(url, targetDir)
    # print (list_fullPath)  
    # #-----extract and sql----------
    for i in range(len(list_fileFullPath)):
        fileFullPath = list_fileFullPath[i]
        extractReport_sql_CA(fileFullPath, dbName)   
# weekly_traderReport_silver()


def weekly_traderReport():
    weekly_traderReport_CA()
    weekly_traderReport_AL()
    weekly_traderReport_gold()
    weekly_traderReport_silver()
    
    
    




#---------------------------------------------------

