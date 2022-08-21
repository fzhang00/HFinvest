# -*- coding: utf-8 -*-
"""
@author: haoli
"""
import sys
sys.path.append("../")
# import const_common as constA
# import Const_NYMEXCOMEX_A as constCOMEX_A

# import requests
# from os import makedirs
# import os.path as myPath
import pandas as pd

# from urllib.request import urlopen, Request
from pathlib import Path 
from datetime import datetime

# import os

import pyodbc
import numpy as np

import time
from selenium import webdriver
# import numpy as np

# import ntpath

# import pyautogui, time
# pyautogui.PAUSE =2.5
#----------------------------------
errorFileTargetDir = '../'
# mydownPy.logError("my test message")
#logError(errorFileTargetDir, msg)
# mydownPy.logError(errorFileTargetDir, "my test message")

import key as pconst
_server = pconst.RYAN_SQL['server']
_username = pconst.RYAN_SQL['username']
_password = pconst.RYAN_SQL['password']  
_database = 'FED' 


pd.set_option('mode.chained_assignment', None)

#--------table name ---------
_sqlTable_FED_SOMA_Asset = 'FED_SOMA_Asset'  

_Dir_SOMA_Asset = './SOMA_Asset' 

"""

"""
def sql_SOMA_asset_weekly(df, dbName):
    df = df.replace({np.NAN: None})
    df[df.columns[1]] = df[df.columns[1]].str.slice(0,60) 
    
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server+';DATABASE='+_database+';UID='+_username+';PWD='+_password)
    cursor = cnxn.cursor()    
    for index, row in df.iterrows():
        dateStr = row[0]     
        query = """DELETE FROM %s where Date = '%s' and [SecurityType] = '%s' ;""" % (dbName, dateStr, row[1])
        cursor.execute(query) 
        params = tuple(row)
        query = """INSERT INTO %s VALUES (?,?,? );""" %(dbName)
        cursor.execute(query, params)        
    cnxn.commit()        
    cursor.close()
    cnxn.close()    
# df = pd.read_csv(_Dir_SOMA_Asset + "/2003-07-09_FED_SOMA_Asset.csv")
# dbName = _sqlTable_FED_SOMA_Asset
# sql_SOMA_asset_weekly(df, dbName)

def extract_allFileSubFolders_toSql(sourceDir):
    # pathlist = Path(sourceDir).glob('**/*.*')
    # pathlist = Path(sourceDir).glob('**/*.xlsx')
    pathlist = Path(sourceDir).glob('**/*.csv')
    for path in pathlist:
         # because path is object not string
         csvFileFullPath = str(path)
         print (csvFileFullPath) 
         df = pd.read_csv(csvFileFullPath)
         dbName = _sqlTable_FED_SOMA_Asset
         sql_SOMA_asset_weekly(df, dbName)         
# csvFileDir = _Dir_SOMA_Asset
# extract_allFileSubFolders_toSql(csvFileDir)

def webpage_table_SOMA_asset(saveDir):  # 2003-07-09
    url = 'https://www.newyorkfed.org/markets/soma-holdings'       
    driver = webdriver.Chrome('../chromedriver.exe')
    driver.implicitly_wait(10) # seconds    
    driver.get(url)
    time.sleep(5)    
# -- start to read webpage
    closeTerm = "cookieButton"
    driver.find_element_by_id(closeTerm).click()
    while (True): # used to download history
        dateStr1 = driver.find_element_by_class_name("datepicker").text
        dd = datetime.strptime(dateStr1, '%B %d, %Y')
        dateStr = dd.strftime('%Y-%m-%d')
        
        tableName = "p-datatable-table.ng-star-inserted"
        webObj = driver.find_element_by_class_name(tableName).get_attribute('outerHTML') 
        
        df = pd.read_html(webObj)[0]  
        df[df.columns[0]] = df[df.columns[0]].str.replace('*','', regex=True)
        df.insert(0, 'Date', dateStr)
        
        csvFileFullPath = saveDir +'/' +  dateStr + '_FED_SOMA_Asset.csv'   
        df.to_csv(csvFileFullPath, index= False) 
        print('FED SOMA asset downloaded: ' + csvFileFullPath)        
        break   # stop looping
    
#-----------end     
        #----move the previous page 
        if dateStr in "2003-07-09":
            driver.quit()
            return          
        tt = "pi.pi-caret-left"
        driver.find_element_by_class_name(tt).click() 
        time.sleep(5)
        #----end move the previous page
    driver.quit()
    return csvFileFullPath

# saveDir = _Dir_SOMA_Asset
# csvFileFullPath = webpage_table_SOMA_asset(saveDir)  
# print()

def SOMA_asset_weekly_Thursday_4PM():
    saveDir = _Dir_SOMA_Asset
    csvFileFullPath = webpage_table_SOMA_asset(saveDir)      

    df = pd.read_csv(csvFileFullPath)
    dbName = _sqlTable_FED_SOMA_Asset
    sql_SOMA_asset_weekly(df, dbName)

SOMA_asset_weekly_Thursday_4PM()



# def makeTodayDataDir(newDir):
#     # if not myPath.lexists(newDir): #lexists
#     if not myPath.exists(newDir):
#         makedirs(newDir)
        

# def getDateFromString(dateStr, keyword): 
#     if keyword == '':
#         d = dateStr
#     else:        
#         b = dateStr.split(keyword)
#         d = b[1].strip()
#         date_fromFile = d
#     try: # DD-MM-YYYY        
#         date_fromFile = datetime.strptime(d, "%m/%d/%Y") #use cme 
#     except ValueError:
#         # try another format
#         try:
#             date_fromFile = datetime.strptime(d, '%d %B %Y') # used LME
#             # d.strftime("%A %d. %B %Y")
#             # 'Monday 11. March 2002'
#         except ValueError:
#             try:
#                 date_fromFile = datetime.strptime(d, '%d %b %Y') # LME gold 01 Apr
#                 # print (datetime.strptime(date_str, "%m-%d"))
#             except ValueError:
#                 try:
#                     # date_fromFile = datetime.strptime(d, '%Y年%m月%d日')  
#                     date_fromFile = datetime.strptime(d, '%b.%d,%Y')  #Date:Mar.05,2021
#                 except ValueError:                
#                     print('9999')
#                     return d
#     return date_fromFile.strftime('%Y-%m-%d')
# # dateStr = 'Data valid for 500 April 2021 '
# # keyword = ''
# # a = getDateFromString(dateStr, keyword)  
# # print(a) 


# def Stock_Industry_lookup(csvFileFullPath, dbName):
#     df = pd.read_csv(csvFileFullPath)  
#     dfdata = df.iloc[: , [2 ,3, 4 ]  ]
#     dfdata['IndustryEng'] = None
#     dfdata = dfdata.replace({np.NAN: None})

#     cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server+';DATABASE='+_database+';UID='+_username+';PWD='+_password)
#     cursor = cnxn.cursor()
#     #---------------     
#     for index, row in dfdata.iterrows():
#         query = """DELETE FROM %s where Ticker = '%s' ;""" % (dbName, row[1])
#         cursor.execute(query) 
        
#         params = tuple(row)
#         query = """INSERT INTO %s VALUES (?,?,?,?);""" %(dbName)
#         cursor.execute(query, params)        
#     cnxn.commit() 
#     #---------------       
#     cursor.close()
#     cnxn.close()
    
# # csvFileFullPath = _Dir_SEC_13F_sina + "/2016-03-31_SEC_13F_sina_Q.csv"
# # dbName = _sqlTable_Stock_Industry_lookup
# # Stock_Industry_lookup(csvFileFullPath, dbName)
# # print()




# def SEC_13F_sina_stock_Q():
#     saveDir = _Dir_SEC_13F_sina
#     csvFileFullPath = webpage_table_13F_sina_stock(saveDir)  
    
#     dbName = _sqlTable_SEC_13F_sina_Stock    
#     SQL_13F_sina_stock(csvFileFullPath, dbName)
    
#     #------industry only-----------
#     dbName = _sqlTable_Stock_Industry_lookup
#     Stock_Industry_lookup(csvFileFullPath, dbName)
# # SEC_13F_sina_stock_Q()





#-------not needed-------




# def webpage_table_13F_sina(saveDir):  
    
#     # file_object = open('./sample.txt', 'a', encoding = 'utf-16')
#     cols = ['Date', "Ticker", "Industry","NumOfHolder","ShareM", 
#             "QoQ","MarketValue_100M","Ratio_InstitutionHolding"]
#     df = pd.DataFrame(columns = cols)  
    
#     url = 'http://global.finance.sina.com.cn/clues/13f/?nav13f_id=SymbolStats'    
#     driver = webdriver.Chrome('chromedriver.exe')
#     driver.get(url)
#     time.sleep(2)
#     nextButton = driver.find_element_by_id("next")
#     dateStr = constA.todayDate_str
    
#     for page in range(100):
#         print ("downloading page: " + str(page) )
#         webObj2 = driver.find_elements_by_xpath("//table[@id= 'SymbolStats']/tbody/tr")
#         numRows = len(webObj2)
#         # webObj = driver.find_element_by_xpath("//*[@id= 'SymbolStats']/tbody/tr[1]/td")
#         webObj = driver.find_elements_by_xpath("//table[@id= 'SymbolStats']/tbody/tr[1]/td")
#         numCols = len(webObj)
        
#         for row in range (numRows):
#             print ('downloading row: ' + str(row) )
#             pathStr = "//table[@id= 'SymbolStats']/tbody/tr[" + str(row+1) + "]/td" 
#             currentRow = driver.find_elements_by_xpath(pathStr)
            
#             li = [dateStr]
#             for col in range (2, numCols-2):
#                 li.append(currentRow[col].text)
#             # print (li)
#             df1 = pd.DataFrame([li], columns = cols) 
#             df = df.append(df1, ignore_index=True)
#         nextButton.click_and_hold() 
#         time.sleep(1)
#         nextButton.release()
#         # nextButton.click()
#         time.sleep(4)    
#     driver.quit()
    
#     csvFileFullPath = saveDir +'/' +  dateStr + '_SEC_13F_sina_Q.csv'   
#     df.to_csv(csvFileFullPath, index= False) 
#     print('SEC_13F_sina downloaded: ' + csvFileFullPath)
#     return csvFileFullPath
# # saveDir = dir_SEC_13F_sina
# # webpage_table_13F_sina(saveDir)    
# # df = pd.read_csv('./sample.txt', sep=" ", header = None, encoding = 'utf-16')    
# # print ()





















