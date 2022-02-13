# -*- coding: utf-8 -*-
"""
@author: haoli
"""
import sys
sys.path.append("../")
import const_common as constA
# import Const_NYMEXCOMEX_A as constCOMEX_A

# import requests
from os import makedirs
import os.path as myPath
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


_Dir_SEC_13F_sina = './SEC_13F_sina'

# mydownPy.logError("my test message")
#logError(errorFileTargetDir, msg)
# mydownPy.logError(errorFileTargetDir, "my test message")

import key as pconst
_server = pconst.RYAN_SQL['server']
_username = pconst.RYAN_SQL['username']
_password = pconst.RYAN_SQL['password']  
_database = 'SEC' 


pd.set_option('mode.chained_assignment', None)

#--------table name ---------
_sqlTable_SEC_13F_sina_Stock = 'SEC_13F_sina_Stock'     

_sqlTable_Stock_Industry_lookup = 'Stock_Industry_lookup'

"""

"""
def makeTodayDataDir(newDir):
    # if not myPath.lexists(newDir): #lexists
    if not myPath.exists(newDir):
        makedirs(newDir)
        

def getDateFromString(dateStr, keyword): 
    if keyword == '':
        d = dateStr
    else:        
        b = dateStr.split(keyword)
        d = b[1].strip()
        date_fromFile = d
    try: # DD-MM-YYYY        
        date_fromFile = datetime.strptime(d, "%m/%d/%Y") #use cme 
    except ValueError:
        # try another format
        try:
            date_fromFile = datetime.strptime(d, '%d %B %Y') # used LME
            # d.strftime("%A %d. %B %Y")
            # 'Monday 11. March 2002'
        except ValueError:
            try:
                date_fromFile = datetime.strptime(d, '%d %b %Y') # LME gold 01 Apr
                # print (datetime.strptime(date_str, "%m-%d"))
            except ValueError:
                try:
                    # date_fromFile = datetime.strptime(d, '%Y年%m月%d日')  
                    date_fromFile = datetime.strptime(d, '%b.%d,%Y')  #Date:Mar.05,2021
                except ValueError:                
                    print('9999')
                    return d
    return date_fromFile.strftime('%Y-%m-%d')
# dateStr = 'Data valid for 500 April 2021 '
# keyword = ''
# a = getDateFromString(dateStr, keyword)  
# print(a) 

def webpage_table_13F_sina_stock(saveDir):   
    url = 'http://global.finance.sina.com.cn/clues/13f/?nav13f_id=SymbolStats'       
    driver = webdriver.Chrome('../chromedriver.exe')
    # driver.implicitly_wait(5) # seconds    
    driver.get(url)
    time.sleep(10)    
    #---MAKE 100 per page
    hover100row = driver.find_element_by_xpath("//*[@id='page_left']/span[4]")     
    #("/html/body/div[10]/div[2]/div[3]/div[1]/span[4]")  //*[@id= 'SymbolStats']/tbody/tr[1]/td"
    hover50row  = driver.find_element_by_xpath("//*[@id='page_left']/span[3]")   
    #("/html/body/div[10]/div[2]/div[3]/div[1]/span[3]")
    # move50row.click()                                 
    # time.sleep(3)
    # hover100row.click()
    action = webdriver.ActionChains(driver)    
    action.move_to_element(hover50row).click(hover50row)    
    action.move_to_element(hover100row).click(hover100row)
    action.perform()
    time.sleep(4)
    action.reset_actions()
  
    time.sleep(4)    
    #-------do not change above-----------    
    # file_object = open('./sample.txt', 'a', encoding = 'utf-16')
    # cols = ['Date',                             "Ticker", "Industry","NumOfHolder","ShareM", 
    #         "QoQ","MarketValue_100M","Ratio_InstitutionHolding"]
    
    cols = ['Date', "RankMarketVauleOfHolding", "Name", "Ticker", "Industry","NumOfHolder","HoldingShareM", 
            "HoldingShareQoQ","MarketValueOfHolding_100M","Ratio_InstitutionHolding", "PriceQoQ"]    
    df = pd.DataFrame(columns = cols)  
    #--------csv file format no change-----------------    

    dateStr = (datetime.today()).strftime( '%Y-%m-%d' )  #'2016-03-31'
    currentYear     = driver.find_element_by_xpath("/html/body/div[10]/div[2]/div[1]/div/div/table/tbody/tr[1]/td[1]/span[1]").text
    currentQuarter  = driver.find_element_by_xpath("/html/body/div[10]/div[2]/div[1]/div/div/table/tbody/tr[2]/td[1]/span").text
    
    if currentQuarter == "Q1":
        currentQuarter = "03-31"
    elif currentQuarter == "Q2":
        currentQuarter = "06-30"
    elif currentQuarter == "Q3":
        currentQuarter = "09-30"
    elif currentQuarter == "Q4":
        currentQuarter = "12-31"        
    reportTime = currentYear.strip() + "-" + currentQuarter.strip()    
    print ("Current quarter:  " + reportTime)
    nextButton = driver.find_element_by_id("next")    
    # webObj = driver.find_element_by_xpath("//*[@id= 'SymbolStats']/tbody/tr[1]/td")
    webObj = driver.find_elements_by_xpath("//table[@id= 'SymbolStats']/tbody/tr[1]/td")     
    numCols = len(webObj)
    
    for page in range(11):
        print ("downloading page: " + str(page+1) )
        webObj2 = driver.find_elements_by_xpath("//table[@id= 'SymbolStats']/tbody/tr")
        numRows = len(webObj2)        
        for row in range (numRows):
            # print ('downloading row: ' + str(row+1) )
            pathStr = "//table[@id= 'SymbolStats']/tbody/tr[" + str(row+1) + "]/td" 
            currentRow = driver.find_elements_by_xpath(pathStr)                          
            li = [reportTime]
            
            for col in range (0, numCols-1):
                # print(currentRow[col].text)
                a = str(currentRow[col].text)
                li.append(a)
            # print (li)
            df1 = pd.DataFrame([li], columns = cols) 
            df = df.append(df1, ignore_index=True)            
        
        # action.move_to_element(nextButton).perform()
        # action.click(nextButton).perform()
        action2 = webdriver.ActionChains(driver)
        action2.move_to_element(nextButton).click(nextButton).perform()
        action2.reset_actions()  
        # action.move_to_element(nextButton)
        # action.click(nextButton) 
        time.sleep(3)
        
    driver.quit()
    
    csvFileFullPath = saveDir +'/' +   reportTime + '_'+ dateStr + '_SEC_13F_sina_Q.csv'   
    df.to_csv(csvFileFullPath, index= False) 
    print('SEC_13F_sina downloaded: ' + csvFileFullPath)
    return csvFileFullPath
# saveDir = _Dir_SEC_13F_sina
# csvFileFullPath = webpage_table_13F_sina_stock(saveDir)  
# print()

def SQL_13F_sina_stock(csvFileFullPath, dbName):
    df = pd.read_csv(csvFileFullPath)  
    df[df.columns[7]]   = df[df.columns[7]].str.rstrip('%')
    df[df.columns[9]]   = df[df.columns[9]].str.rstrip('%')
    df[df.columns[10]]  = df[df.columns[10]].str.rstrip('%')
        # df[col] = pd.to_numeric(df[col], errors='coerce',downcast= 'integer')  
    for i in range(len(df)):
        try:
            float(df.iat[i, 7])            
        except ValueError:
            df.iat[i, 7] = None
        try:
            float(df.iat[i, 9])            
        except ValueError:
            df.iat[i, 9] = None
        try:
            float(df.iat[i, 10])            
        except ValueError:
            df.iat[i, 10] = None            
    dfdata = df.iloc[: , [0,1, 3, 5,6,7,8,9,10]  ]
    dfdata = dfdata.replace({np.NAN: None})

    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server+';DATABASE='+_database+';UID='+_username+';PWD='+_password)
    cursor = cnxn.cursor()
    #--------------- 
    dateStr = dfdata.iat[0,0]
    query = """DELETE FROM %s where Date = '%s' ;""" % (dbName, dateStr)
    cursor.execute(query)    
    
    for index, row in dfdata.iterrows():
        params = tuple(row)
        query = """INSERT INTO %s VALUES (?,?,?,?, ?,?,?,?, ? );""" %(dbName)
        cursor.execute(query, params)        
    cnxn.commit() 
    #---------------       
    cursor.close()
    cnxn.close()
    # print ("----SEC 13F stock database updated : " +  (datetime.today()).strftime('%Y-%m-%d') )
    print ("----SEC 13F stock database updated : " +  dateStr)
   
# csvFileFullPath = _Dir_SEC_13F_sina + "/2016-03-31_SEC_13F_sina_Q.csv"
# dbName = _sqlTable_SEC_13F_sina_Stock
# SQL_13F_sina_stock(csvFileFullPath, dbName)
# print()

def Stock_Industry_lookup(csvFileFullPath, dbName):
    df = pd.read_csv(csvFileFullPath)  
    dfdata = df.iloc[: , [2 ,3, 4 ]  ]
    dfdata['IndustryEng'] = None
    dfdata = dfdata.replace({np.NAN: None})

    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server+';DATABASE='+_database+';UID='+_username+';PWD='+_password)
    cursor = cnxn.cursor()
    #---------------     
    for index, row in dfdata.iterrows():
        query = """DELETE FROM %s where Ticker = '%s' ;""" % (dbName, row[1])
        cursor.execute(query) 
        
        params = tuple(row)
        query = """INSERT INTO %s VALUES (?,?,?,?);""" %(dbName)
        cursor.execute(query, params)        
    cnxn.commit() 
    #---------------       
    cursor.close()
    cnxn.close()
    
# csvFileFullPath = _Dir_SEC_13F_sina + "/2016-03-31_SEC_13F_sina_Q.csv"
# dbName = _sqlTable_Stock_Industry_lookup
# Stock_Industry_lookup(csvFileFullPath, dbName)
# print()

def extract_allFileSubFolders_toSql(sourceDir):
    # pathlist = Path(sourceDir).glob('**/*.*')
    # pathlist = Path(sourceDir).glob('**/*.xlsx')
    pathlist = Path(sourceDir).glob('**/*.csv')
    for path in pathlist:
         # because path is object not string
         csvFileFullPath = str(path)
         print (csvFileFullPath)
         
         dbName = _sqlTable_SEC_13F_sina_Stock
         SQL_13F_sina_stock(csvFileFullPath, dbName)

         #------industry only-----------
         dbName = _sqlTable_Stock_Industry_lookup
         Stock_Industry_lookup(csvFileFullPath, dbName)
         
# csvFileDir = _Dir_SEC_13F_sina + "/workDir"
# extract_allFileSubFolders_toSql(csvFileDir)
# print()


def SEC_13F_sina_stock_Q():
    saveDir = _Dir_SEC_13F_sina
    csvFileFullPath = webpage_table_13F_sina_stock(saveDir)  
    
    dbName = _sqlTable_SEC_13F_sina_Stock    
    SQL_13F_sina_stock(csvFileFullPath, dbName)
    
    #------industry only-----------
    dbName = _sqlTable_Stock_Industry_lookup
    Stock_Industry_lookup(csvFileFullPath, dbName)
SEC_13F_sina_stock_Q()


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





















