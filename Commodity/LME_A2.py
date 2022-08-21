# -*- coding: utf-8 -*-
"""
@author: haoli

"""

import sys
sys.path.append("../")

import const_common as constA
import downloadUpdateData as mydownPy

import Const_LME_A2 as constLME_a2


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
from selenium.common.exceptions import NoSuchElementException

from datetime import datetime
import ntpath

from pathlib import Path

import pyodbc
import numpy as np

#----------------------------------
errorFileTargetDir = '../'

# _dateSearchBy_ClassName_nonFerrous_gold_silver = "delayed-date.left"
_dateSearchBy_xpath = "/html/body/main/div[1]/div/div/div[2]/div[1]/div/div[1]/span[3]"  #"delayed-date.left"
# _dateSearchBy_xpath2 = "/html/body/main/div[1]/div[4]/div/div[2]/div[1]/div/div[1]/span[3]"

# global dateBackupNickleStr

_dateSearchKeyword = "Data valid for"

_waitTime_loadWebsite_LME = 3

_columnName_goldSilver = ['Date', 'Volume', 'Open Interest']

import key as pconst
_server = pconst.RYAN_SQL['server']
_database = pconst.RYAN_SQL['database']
_username = pconst.RYAN_SQL['username']
_password = pconst.RYAN_SQL['password']      

_sqlTable_LME_baseMetal_stock               = 'LME_baseMetal_stock'
_sqlTable_LME_baseMetal_OfficialPrice2021   = 'LME_baseMetal_OfficialPrice2021'
_sqlTable_LME_baseMetal_ColsePrice2021      = 'LME_baseMetal_ColsePrice2021'


_sqlTable_LME_precious_steel_price2021  = 'LME_precious_steel_price2021'
_sqlTable_LME_Lithium_ColsePrice2021    = 'LME_Lithium_ColsePrice2021'
# _sqlTable_LME_precious_VolOpenInterest = 'LME_precious_VolOpenInterest_M'


#------- ---------

# mydownPy.logError("my test message")
#logError(errorFileTargetDir, msg)
# mydownPy.logError(errorFileTargetDir, "my test message")

def makeTodayDataDir(newDir):
    # if not myPath.lexists(newDir): #lexists
    if not myPath.exists(newDir):
        makedirs(newDir)

def whitespace_remover(dataframe):
    for i in dataframe.columns:
        if dataframe[i].dtype == 'object': # applying strip function on column
            dataframe[i] = dataframe[i].map(str.strip)
        else: # if condn. is False then it will do nothing.
            pass
        
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
# keyword = 'Data valid for'
# dateStr = '01 Apr'
# dateStr = '2021年04月16日'
# keyword = ''
# a = getDateFromString(dateStr, keyword)  
# print(a)   
# def dateSearch_LME(dateSearchBy, dateStr):
#     if dateSearchBy == _dateSearchBy_ClassName_nonFerrous_gold_silver: 
#         dateStr = getDateFromString(dateStr, _dateSearchKeyword)
#     else:
#         pass    
#     return dateStr

def convertDDMM_date(df, convertByColnumNum):
    num = convertByColnumNum
    for i in range(len(df)): 
        dateStr = df.iloc[i][num]
        yy = datetime.strptime(dateStr, '%d %B %Y').strftime('%Y-%m-%d')
        df.iat[i, num] = yy
    return df

# timeRef = '2021-03-06' 
# convertDDMM_date(df, timeRef)

#--------------------------------------

def sql_NonFerrous_HTML_Stock_Price1(htmlFileFullPath, metalName, date_fromFolderName):
    myDataFrameLists = pd.read_html(htmlFileFullPath)   
    if len(myDataFrameLists) == 0:
        msg = "empty Stock table from website: " + htmlFileFullPath
        mydownPy.logError(errorFileTargetDir, msg) 
        print ("error:  empty Stock table from website: " + htmlFileFullPath)
        return
    else: 
        # htmlFilePath = constA.getFilePathInfo(htmlFileFullPath, 0) #/temp/2021-04-01
        # metalName    = constA.getFilePathInfo(htmlFileFullPath, 2).strip()
        # date_fromFolderName  = constA.getFilePathInfo(htmlFilePath, 1) #2021-04-01
            
        
        #----------build the dataframe and save it
        df_price = (myDataFrameLists[0])
        df_price = df_price.replace({np.NAN: None}) 
        # df_price = df_price.replace({np.NAN: r'NULL})         
        df_OfficialPrice = df_price.iloc[:, 1:]

        df_ClosePrice = (myDataFrameLists[1])
        df_ClosePrice = df_ClosePrice.replace({np.NAN: None}) 
        
        df_stock = (myDataFrameLists[2])
        df_stock = df_stock.replace({np.NAN: None})
        # whitespace_remover(df_stock)
        
        # ----- connect the database        
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server+';DATABASE='+_database+';UID='+_username+';PWD='+_password)
        cursor = cnxn.cursor()        
         #----------table stock ---
        query = """DELETE FROM %s where Date = '%s' and Future = '%s' ;""" % (_sqlTable_LME_baseMetal_stock, date_fromFolderName, metalName)
        cursor.execute(query)  
        params = (date_fromFolderName, metalName)
        count = 0
        for (columnName, columnData) in df_stock.iteritems():
            if count >0: # remove the first column of names
                params1 = tuple(columnData)
                params =  params + params1   
            count +=1 
        query = """INSERT INTO %s VALUES (?,?,?,?, ?);""" %(_sqlTable_LME_baseMetal_stock)
        cursor.execute(query, params)                       
        cnxn.commit() 
        
         #----------table official prices ---
        query = """DELETE FROM %s where Date = '%s' and Contract = '%s' ;""" % (_sqlTable_LME_baseMetal_OfficialPrice2021, date_fromFolderName, metalName)
        cursor.execute(query)         
        params = (date_fromFolderName, metalName)        
        for (index, data) in df_OfficialPrice.iterrows():              
            params1 = tuple(data)
            params =  params + params1
            # query = """INSERT INTO %s ([Date], Contract, CashBuyer, CashSellerSettlement, Month3_Buyer, Month3_Seller, Month15_Buyer, Month15_Seller, Dec1_Buyer, Dec1_Seller) VALUES (?,?,?,?,  ?,?,?,?, ?,? );""" %(_sqlTable_LME_baseMetal_price)
        if metalName.lower() == "tin" or metalName.lower() == "aluminium alloy" or metalName.lower() == "nasaac" or metalName.lower() == "cobalt":
            # a = ("NULL", "NULL","NULL","NULL")
            a = (None, None,None,None)
            # a = ('None', 'None','None','None')
            # a = ('Nan', 'Nan','Nan','Nan')
            params = params + a
        query = """INSERT INTO %s VALUES (?,?,?,?, ?,?,?,?, ?,?,?,? );""" %(_sqlTable_LME_baseMetal_OfficialPrice2021)
        # query = """INSERT INTO %s VALUES  %s ;""" %(_sqlTable_LME_baseMetal_price, params)
        cursor.execute(query, params)
        cnxn.commit() 
        
        #----------table closing prices ---
        query = """DELETE FROM %s where Date = '%s' and Contract = '%s';""" % (_sqlTable_LME_baseMetal_ColsePrice2021, date_fromFolderName, metalName)
        cursor.execute(query)  
        

        params = (date_fromFolderName, metalName)        
        count = 0
        for (columnName, columnData) in df_ClosePrice.iteritems():
            if count >0: # remove the first column of names

                if metalName.lower() == "cobalt":
                    a = (columnData[0],columnData[1],columnData[2],columnData[3], None, columnData[4],columnData[5])
                    params =  params + (a)
                    pass
                else:
                    params1 = tuple(columnData)
                    params =  params + params1             
                # a = (date_fromFolderName, metalName)
                # params = (a + tuple(columnData))                 
            count +=1            
        query = """INSERT INTO %s VALUES (?,?,?,?, ?,?,?,?, ?);""" %(_sqlTable_LME_baseMetal_ColsePrice2021)
        cursor.execute(query, params)         
        cnxn.commit()         
        # -----close database connection ----------G:\Projects\HFinvest\Commodity\data\LME\temp_A\2022-01-24\Aluminium.html
        
        cursor.close()
        cnxn.close()        
# htmlFileFullPath = constLME_a2.commodityLME_workDir_A +'/2021-09-17/Cobalt.html'
# htmlFileFullPath = constLME_a2.commodityLME_workDir_A +'/2022-01-21/Cobalt.html'
# sql_NonFerrous_HTML_Stock_Price1(htmlFileFullPath)
# print()       

def sql_Gold_Silver_Steel_HTML_Price(htmlFileFullPath, metalName, date_fromFolderName):
    myDataFrameLists = pd.read_html(htmlFileFullPath)   
    if len(myDataFrameLists) == 0:
        msg = "empty Stock table from website: " + htmlFileFullPath
        mydownPy.logError(errorFileTargetDir, msg)  
        print("error: empty Stock table from website  " + htmlFileFullPath)
        return
    else: 
        # htmlFilePath = constA.getFilePathInfo(htmlFileFullPath, 0) #/temp/2021-04-01
        # metalName    = constA.getFilePathInfo(htmlFileFullPath, 2).strip()
        # date_fromFolderName  = constA.getFilePathInfo(htmlFilePath, 1) #2021-04-01
              
        #----------build the dataframe and save it
        df_ClosePrice = (myDataFrameLists[0])
        df_ClosePrice = df_ClosePrice.replace({np.NAN: None}) 
        # whitespace_remover(df_stock)

        # ----- connect the database        
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server+';DATABASE='+_database+';UID='+_username+';PWD='+_password)
        cursor = cnxn.cursor()          
        #----------table closing prices ---
        query = """DELETE FROM %s where Date = '%s' and Contract = '%s';""" % (_sqlTable_LME_precious_steel_price2021, date_fromFolderName, metalName)
        cursor.execute(query) 
        
        if metalName.lower() == "steel rebar":
            params = (date_fromFolderName, metalName, None)
        else:
            params = (date_fromFolderName, metalName)            
        count = 0
        for (columnName, columnData) in df_ClosePrice.iteritems():
            if count >0: # remove the first column of names
                params1 = tuple(columnData)
                params =  params + params1             
                # a = (date_fromFolderName, metalName)
                # params = (a + tuple(columnData))
            count +=1             
        if metalName.lower() == "steel rebar":
            a = (None, None, None, None, None, None, None, None, None)
            params = params + a 
        query = """INSERT INTO %s VALUES (?,?,?,?, ?,?,?,?, ?,?,?,?, ?,?,?,?, ?,?,?,?, ?,?,?,?, ?,?,?);""" %(_sqlTable_LME_precious_steel_price2021)
        cursor.execute(query, params)         
        cnxn.commit()         
        # -----close database connection ----------
        cursor.close()
        cnxn.close()    
# htmlFileFullPath = constLME_a2.commodityLME_workDir_A +'/2021-09-17/Steel Rebar.html'
# sql_Gold_Silver_Steel_HTML_Price(htmlFileFullPath)
# print()    
def sql_Lithium_HTML_Price(htmlFileFullPath, metalName):
    myDataFrameLists = pd.read_html(htmlFileFullPath)   
    if len(myDataFrameLists) == 0:
        msg = "empty Stock table from website: " + htmlFileFullPath
        mydownPy.logError(errorFileTargetDir, msg)  
        return
    else: 
        # htmlFilePath = constA.getFilePathInfo(htmlFileFullPath, 0)
        # metalName    = constA.getFilePathInfo(htmlFileFullPath, 2).strip()
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
# htmlFileFullPath = constLME_a2.commodityLME_workDir_A +'/2021-09-17/Lithium.html'
# sql_Lithium_HTML_Price(htmlFileFullPath)
# print()       
dateBackupNickleStr = '2022-03-25'
def saveWebPage_nonFerrous_gold_Silver(url, destFilePath, destFileName, dateSearchBy, waitTime_loadWebsite): 
    global dateBackupNickleStr
    driver = webdriver.Chrome('chromedriver.exe')
    driver.implicitly_wait(10)    
    driver.get(url)
    time.sleep(3)    
    # from selenium.common.exceptions import NoSuchElementException
    try:
        driver.find_element_by_id("onetrust-accept-btn-handler").click()
        # elem = driver.find_element_by_xpath(".//*[@id='SORM_TB_ACTION0']")
        # elem.click()
    except NoSuchElementException:  #spelling error making this code not work as expected
        pass
    # driver.find_element_by_id("onetrust-accept-btn-handler").click() 
    time.sleep(3)    
        # pyautogui.hotkey("f5")
        # time.sleep(waitTime_loadWebsite)
    
    #-------get the date information
    if destFileName == constLME_a2.Key_Lithium :
        dateStr = constA.todayDate_str # weekly data no date infor in webpage
        pass
    elif destFileName == constLME_a2.Key_Nickel:
        dateStr = dateBackupNickleStr
        pass    
    else:
        # try:
        #     date_field = driver.find_element_by_xpath(dateSearchBy)
        #     # print(date_field.text)
        #     dateStr1 = date_field.text    
        #     dateStr = getDateFromString(dateStr1, _dateSearchKeyword)
        #     # dateStr = dateSearch_LME(dateSearchBy, dateStr)
                     
            
        # except NoSuchElementException:  #spelling error making this code not work as expected
        #     pass 
        # dateBackupNickleStr = dateStr   
        
        date_field = driver.find_element_by_xpath(dateSearchBy)
        dateStr1 = date_field.text    
        dateStr = getDateFromString(dateStr1, _dateSearchKeyword)
        
    # -------- make file dir, delete old file and set the file name   
    destFilePath_2 = destFilePath + '/' + dateStr  
    makeTodayDataDir(destFilePath_2)    

    fileFullPath = destFilePath_2 + '/' + destFileName + '.html' 
    # fileFullPath = destFilePath_2 + '/' + destFileName
    if os.path.isfile(fileFullPath):
        os.remove(fileFullPath)
        print('file removed: ' + fileFullPath)
        time.sleep(3)
        
    #-----convert python dir to windows dir 
    fileAbsPath = os.path.abspath(fileFullPath)   
    winPath = fileAbsPath.replace(os.sep,ntpath.sep)
    
    pyautogui.hotkey('ctrl', 's')
    time.sleep(2)
    
    pyautogui.typewrite(winPath)
    time.sleep(2)
    
    pyautogui.hotkey('enter')   
    time.sleep(20)
    driver.quit()
    #--------------------check if the file is download with data
    # fileSize = os.stat(fileFullPath).st_size
    # if fileSize < 1000: # 5k
    #     msg = "website download data <1K: " + fileFullPath + " ; url: " + url 
    #     mydownPy.logError(errorFileTargetDir, msg)
    # else: # save, update the data
    #     print('file donwloaded: ' + url)    G:\Projects\HFinvest\Commodity\data\LME\temp_A\2022-03-25\Nickel.html
    

    # tables = pd.read_html(driver.page_source)
    
    
    if destFileName == constLME_a2.Key_Nickel:
        print("LME_A2 download no sql: "+ destFileName)
        return fileFullPath
    
    htmlFileFullPath = driver.page_source    
    metalName    =  destFileName  
    date_fromFolderName = dateStr
    if metalName.lower() == constLME_a2.KEY_Gold.lower() or metalName.lower() == constLME_a2.KEY_Silver.lower() or metalName.lower() == constLME_a2.Key_SteelRebar.lower() :
        sql_Gold_Silver_Steel_HTML_Price(htmlFileFullPath, metalName, date_fromFolderName) 
        pass 
    elif (metalName.lower() == constLME_a2.Key_Lithium.lower()):
        sql_Lithium_HTML_Price(htmlFileFullPath, metalName)
        pass
    else:
        sql_NonFerrous_HTML_Stock_Price1(htmlFileFullPath, metalName, date_fromFolderName)
        pass  
    
       
        
    print("LME_A2 download : "+ destFileName)
    return fileFullPath

# url =  constLME_a2.DICT_URL_A.get(constLME_a2.KEY_Gold)
# destFilePath =  constLME_a2.commodityLME_workDir_A
# destFileName =  constLME_a2.KEY_Gold
# # dateSearchBy =  "/html/body/main/div[1]/div/div/div[2]/div[1]/div/div[1]/span[3]"
# dateSearchBy =  _dateSearchBy_xpath
# waitTime_loadWebsite = _waitTime_loadWebsite_LME
# saveWebPage_nonFerrous_gold_Silver(url, destFilePath, destFileName, dateSearchBy, waitTime_loadWebsite) 
# print()

def daily_save_sql_webPages_nonFerrous_gold_Silver_Steel():  
    destFilePath =  constLME_a2.commodityLME_workDir_A
    dateSearchBy =  _dateSearchBy_xpath 
    waitTime_loadWebsite = _waitTime_loadWebsite_LME   
    
    #------------do not change-------    
    for key, value in constLME_a2.DICT_URL_A.items():
        url = value
        destFileName = key
        htmlFileFullPath = saveWebPage_nonFerrous_gold_Silver(url, destFilePath, destFileName, dateSearchBy, waitTime_loadWebsite) 
        # # li = [] li.append(htmlFileFullPath)         
# daily_save_sql_webPages_nonFerrous_gold_Silver_Steel()
# print()

def weekly_save_sql_webPage_Lithium():
    destFilePath =  constLME_a2.commodityLME_workDir_A
    dateSearchBy =  _dateSearchBy_xpath 
    waitTime_loadWebsite = _waitTime_loadWebsite_LME    
    url = constLME_a2.Lithium_url
    destFileName = constLME_a2.Key_Lithium
    
    htmlFileFullPath = saveWebPage_nonFerrous_gold_Silver(url, destFilePath, destFileName, dateSearchBy, waitTime_loadWebsite) 
    # sql_Lithium_HTML_Price(htmlFileFullPath)
# weekly_save_sql_webPage_Lithium()
# print()     
   
def LME_A_daily_Run():    
    if datetime.today().weekday() == 5:# or datetime.today().weekday() == 6:
        weekly_save_sql_webPage_Lithium()
    elif datetime.today().weekday() == 6:
        pass
    else:    
        daily_save_sql_webPages_nonFerrous_gold_Silver_Steel()     
# daily_save_sql_webPages_nonFerrous_gold_Silver_Steel()    
# weekly_save_sql_webPage_Lithium()
LME_A_daily_Run()


def subFolders_toSql(sourceDir):  # not updated no working
    pathlist = Path(sourceDir).glob('**/*.html')
    for path in pathlist:
         # because path is object not string
         htmlFileFullPath = str(path)
         
         if 'saved_resource' in htmlFileFullPath: # there is saved_resource.html in the folder
             pass
         else:
             htmlFileName = constA.getFilePathInfo(htmlFileFullPath, 1)            
             
             fileAbsPath = os.path.abspath(htmlFileFullPath)   
             winPath = fileAbsPath.replace(os.sep,ntpath.sep)             
             url = winPath
             print (url)
             
             # destFilePath =  constLME_a2.commodityLME_workDir_A + '/workFolder'
             # destFilePath =  constLME_a2.commodityLME_workDir_A
             # destFileName =  htmlFileName
             # # dateSearchBy =  _dateSearchBy_ClassName_nonFerrous_gold_silver 
             # waitTime_loadWebsite = 1 
             
             # htmlFileFullPath = saveWebPage_nonFerrous_gold_Silver(url, destFilePath, destFileName, dateSearchBy, waitTime_loadWebsite) 

             if 'nonferrous' in htmlFileName.lower()  :
                # htmlFileFullPath = saveWebPage_nonFerrous_gold_Silver(url, destFilePath, destFileName, dateSearchBy, waitTime_loadWebsite) 
 
                print('SQL: --' + htmlFileFullPath) 
                sql_NonFerrous_HTML_Stock_Price1(htmlFileFullPath)
                
             elif 'gold' in htmlFileName.lower() or 'silver' in htmlFileName.lower() :
                # htmlFileFullPath = saveWebPage_nonFerrous_gold_Silver(url, destFilePath, destFileName, dateSearchBy, waitTime_loadWebsite) 
 
                # sql_goldSilver_HTML_Price_Vol_OI(htmlFileFullPath)  
                pass
             else:
                # htmlFileFullPath = saveWebPage_nonFerrous_gold_Silver(url, destFilePath, destFileName, dateSearchBy, waitTime_loadWebsite) 
                # sql_NonFerrous_HTML_Stock_Price1(htmlFileFullPath)
                pass
# sourceDir = constLME_a2.commodityLME_workDir_A+ '/workFolder'
# subFolders_toSql(sourceDir) 
# print()  
