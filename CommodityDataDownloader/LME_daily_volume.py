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
# from datetime import datetime
# import ntpath

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

_sqlTable_LME_daily_Volume = 'LME_Daily_Volume'
#------- ---------

# mydownPy.logError("my test message")
#logError(errorFileTargetDir, msg)
# mydownPy.logError(errorFileTargetDir, "my test message")

def makeTodayDataDir(newDir):
    # if not myPath.lexists(newDir): #lexists
    if not myPath.exists(newDir):
        makedirs(newDir)

def convertDDMM_date(df):
    for i in range(len(df)): 
        d = df.iloc[i][0]
        d2 = d.split(':')
        dateStr = d2[0].strip()
        df.iat[i, 0] = dateStr
    return df    

#--------------------------------------
def sql_dailyVolume(df, dbName): 
    # --- SQL ----
    df = df.replace({np.NAN: None})
    
    df[df.columns[2]] = df[df.columns[2]].str.slice(0,44)
    
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server+';DATABASE='+_database+';UID='+_username+';PWD='+_password)
    cursor = cnxn.cursor()
    
    for index, row in df.iterrows():
        dateStr = row[0]
        productStr = row[1] 
        descriptionStr  = row[2]       
        query = """DELETE FROM %s where Date = '%s' and [Product] = '%s' and [Description] = '%s' ;""" % (dbName, dateStr, productStr, descriptionStr)
        cursor.execute(query)         

        params = tuple(row)
        query = """INSERT INTO %s VALUES (?,?,?,? );""" %(dbName)
        cursor.execute(query, params)        
    cnxn.commit()        
    cursor.close()
    cnxn.close()  
    
    
def extractVolumeData_sql(fileFullPath, dbName):
    df = pd.read_excel(fileFullPath, dtype = object)
    df1 = df.dropna(how='all')
    df2 = df1.dropna(axis = 1, how='all')
    df3 = df2.iloc[2:-1]
    df4 = df3.fillna('NA')
    
#-------convert date to yy-mm-dd
    df4[df4.columns[0]] = df4[df4.columns[0]].astype(str)
    df5 = convertDDMM_date(df4)
    df5.columns = df2.iloc[1,:]    
    df_data = df5
        
    dateStr = df_data.iloc[1,0]
    filePath = constA.getFilePathInfo(fileFullPath, 0)
    fileFullPath_new = filePath + '/' + dateStr + '.csv'    

    df_data.to_csv(fileFullPath_new, index = False)    
    print ("daily volume file processed: " + fileFullPath)
    
    #--------sql--------
    df = df_data
    sql_dailyVolume(df, dbName)   
    

# fileFullPath = constLME_a.commodityLME_dailyVolumeDir +'/Daily Volumes - 21 April 2021.xlsx'
# dbName = _sqlTable_LME_daily_Volume
# extractVolumeData_sql(fileFullPath, dbName)
# print()


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
    # outfile.closed
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

def extract_allExcelFileSubFolders_toSql(sourceDir, dbName):
    # pathlist = Path(sourceDir).glob('**/*.*')
    # pathlist = Path(sourceDir).glob('**/*.xlsx')
    pathlist = Path(sourceDir).glob('**/*.xlsx')
    for path in pathlist:
         # because path is object not string
         excelFileFullPath = str(path)
         extractVolumeData_sql(excelFileFullPath, dbName)
         
# sourceDir = constLME_a.commodityLME_dailyVolumeDir + '/2019-2021'
# dbName = _sqlTable_LME_daily_Volume
# extract_allExcelFileSubFolders_toSql(sourceDir, dbName)


def download_href_traderReport_weekly(url, targetDir):
    driver = webdriver.Chrome('chromedriver.exe')
    driver.get(url)
    time.sleep(2) 

    elems = driver.find_elements_by_tag_name('a')
    time.sleep(2)
    count_First10File = 0
    list_fullPath = []    
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
            if count_First10File >9:
                # print('no more the href')
                break                
    driver.quit()    
    time.sleep(1)
    return list_fullPath


# url = 'https://www.lme.com/LME-Clear/Technology/Reports/Volumes'  
# # url = constLME_a.dialyVolume_url
# targetDir = constLME_a.commodityLME_dailyVolumeDir
# list_fullPath = download_href_traderReport_weekly(url, targetDir)
# print (list_fullPath)

def LME_volume_daily_run():
    
    url = constLME_a.dialyVolume_url
    targetDir = constLME_a.commodityLME_dailyVolumeDir
    list_fullPath = download_href_traderReport_weekly(url, targetDir)    

    #------extract files-----------
    for i in range (len(list_fullPath)):        
        fileFullPath = list_fullPath[i]
        dbName = _sqlTable_LME_daily_Volume
        extractVolumeData_sql(fileFullPath, dbName)

# LME_volume_daily_run()
#----------------------------------------------------------------


 
def Workingbackup_download_href_traderReport_weekly(url, targetDir):
    driver = webdriver.Chrome('chromedriver.exe')
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


    
    




#---------------------------------------------------

