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
_sqlTable_LME_precious_VolOpenInterest = 'LME_precious_VolOpenInterest_M'



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
def dateSearch_LME(dateSearchBy, dateStr):
    if dateSearchBy == _dateSearchBy_ClassName_nonFerrous_gold_silver: 
        dateStr = getDateFromString(dateStr, _dateSearchKeyword)
    else:
        pass    
    return dateStr

def convertDDMM_date(df, timeRef, convertByColnumNum):
    yy = timeRef.split('-')
    year = yy[0]
    year1 = str(int(year) - 1)  
    # num = df.columns.get_loc('Date')  
    num = convertByColnumNum
    for i in range(len(df)): 
        dateStr = df.iloc[i][num] + ' ' + year 
        dateStr1 = df.iloc[i][num] + ' ' + year1 
        yy = datetime.strptime(dateStr, '%d %b %Y').strftime('%Y-%m-%d')
        if yy <= timeRef:
            df.iat[i, num] = yy
        else:
            yy = datetime.strptime(dateStr1, '%d %b %Y').strftime('%Y-%m-%d')        
            df.iat[i, num] = yy
    # df.set_index('Date', inplace = True)    
    #     print()
    # print()
    return df

# import pandas as pd
# df = pd.read_csv('testFile_date.csv')
# timeRef = '2021-03-06' 
# convertDDMM_date(df, timeRef)

#--------------------------------------

def sql_NonFerrous_HTML_Stock_Price1(htmlFileFullPath):
    myDataFrameLists = pd.read_html(htmlFileFullPath)   
    if len(myDataFrameLists) == 0:
        msg = "empty Stock table from website: " + htmlFileFullPath
        mydownPy.logError(errorFileTargetDir, msg)  
        return
    else: 
        htmlFilePath = constA.getFilePathInfo(htmlFileFullPath, 0) #/temp/2021-04-01
        date_fromFolderName  = constA.getFilePathInfo(htmlFilePath, 1) #2021-04-01
              
        #----------build the dataframe and save it
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server+';DATABASE='+_database+';UID='+_username+';PWD='+_password)
        cursor = cnxn.cursor()    
        
         #----------table 1 ---
        query = """DELETE FROM %s where Date = '%s';""" % (_sqlTable_LME_baseMetal_price, date_fromFolderName)
        cursor.execute(query)           
        
        df_price = (myDataFrameLists[0])
        df_price = df_price.replace({np.NAN: None}) 
        # whitespace_remover(df_price)
        # df_price = df_price.replace({np.NAN: r'NULL}) 
        count = 0
        for (columnName, columnData) in df_price.iteritems():
            if count >0:
                a = (date_fromFolderName, columnName.strip())
                params = (a + tuple(columnData))
                # query = """INSERT INTO %s ([Date], Contract, CashBuyer, CashSellerSettlement, Month3_Buyer, Month3_Seller, Month15_Buyer, Month15_Seller, Dec1_Buyer, Dec1_Seller) VALUES (?,?,?,?,  ?,?,?,?, ?,? );""" %(_sqlTable_LME_baseMetal_price)
                query = """INSERT INTO %s VALUES (?,?,?,?, ?,?,?,?, ?,? );""" %(_sqlTable_LME_baseMetal_price)
                # query = """INSERT INTO %s VALUES  %s ;""" %(_sqlTable_LME_baseMetal_price, params)
                cursor.execute(query, params)
            count +=1
        cnxn.commit()  

         #----------table 2 ---
        query = """DELETE FROM %s where Date = '%s';""" % (_sqlTable_LME_baseMetal_stock, date_fromFolderName)
        cursor.execute(query)          
        
        df_stock = (myDataFrameLists[1])
        df_stock = df_stock.replace({np.NAN: None})
        # whitespace_remover(df_stock)
        
        count = 0
        for (columnName, columnData) in df_stock.iteritems():
            if count >0:
                a = (date_fromFolderName, columnName.strip())
                params = (a + tuple(columnData))
                query = """INSERT INTO %s VALUES (?,?,?,?, ?);""" %(_sqlTable_LME_baseMetal_stock)
                cursor.execute(query, params)
            count +=1
        cnxn.commit()         
        
        cursor.close()
        cnxn.close()  
        
# htmlFileFullPath = destFilePath =  constLME_a.commodityLME_workDir_A +'/2021-04-28/London Metal Exchange_ Non-ferrous.html'
# sql_NonFerrous_HTML_Stock_Price1(htmlFileFullPath)
# print()       

def sql_goldSilver_HTML_Price_Vol_OI(htmlFileFullPath):
    myDataFrameLists = pd.read_html(htmlFileFullPath)   
    if len(myDataFrameLists) == 0:
        msg = "empty Stock table from website: " + htmlFileFullPath
        mydownPy.logError(errorFileTargetDir, msg)  
        return
    else: 
        htmlFilePath = constA.getFilePathInfo(htmlFileFullPath, 0) #/temp/2021-04-01
        date_fromFolderName  = constA.getFilePathInfo(htmlFilePath, 1) #2021-04-01   
        
        if 'gold' in htmlFileFullPath.lower():
            nameStr = 'Gold'
        elif 'silver' in htmlFileFullPath.lower():
            nameStr = 'Silver'
        else:
            nameStr = 'unknow'
 
        #----------save to sql          
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server+';DATABASE='+_database+';UID='+_username+';PWD='+_password)
        cursor = cnxn.cursor()        
          #----------table 1 ---         
        query = """DELETE FROM %s where Date = '%s' and [Future] = '%s' ;""" % (_sqlTable_LME_precious_price, date_fromFolderName, nameStr)
        cursor.execute(query)  
        df_price = myDataFrameLists[0]
        df_price = df_price.replace({np.NAN: None})
        # whitespace_remover(df_price)
        
        
        a = (date_fromFolderName, nameStr)
        params = (a + tuple(df_price[df_price.columns[1]]) )
        # query = """INSERT INTO %s ([Date], Contract, CashBuyer, CashSellerSettlement, Month3_Buyer, Month3_Seller, Month15_Buyer, Month15_Seller, Dec1_Buyer, Dec1_Seller) VALUES (?,?,?,?,  ?,?,?,?, ?,? );""" %(_sqlTable_LME_baseMetal_price)
        query = """INSERT INTO %s VALUES (?,?,?,?, ?,?,? );""" %(_sqlTable_LME_precious_price,)
        # query = """INSERT INTO %s VALUES  %s ;""" %(_sqlTable_LME_baseMetal_price, params)
        cursor.execute(query, params)        
        cnxn.commit()        
        # cursor.close()
        # cnxn.close()  
         
        #--part 2:---------------------------
        df_Vol_OI = (myDataFrameLists[1]) 
        df_Vol_OI = df_Vol_OI.replace({np.NAN: None}) 
        # whitespace_remover(df_Vol_OI)
        
        convertDateByColNum = 0
        df_Vol_OI_updated = convertDDMM_date(df_Vol_OI, date_fromFolderName, convertDateByColNum)
        
        df_Vol_OI_updated =  df_Vol_OI_updated.sort_values(df_Vol_OI_updated.columns[convertDateByColNum])
        df_Vol_OI_2 = df_Vol_OI_updated .iloc[:-1]
        
        for index, row in df_Vol_OI_2.iterrows(): #: #dfvolOI.iterrows():   
            # print (row)
            # row
            query = """DELETE FROM %s where Date = '%s' and [Future] = '%s' ;""" %  (_sqlTable_LME_precious_VolOpenInterest, row[0], nameStr)
            cursor.execute(query)
            query = """INSERT INTO %s ([Date], [Future], [Volume], [OpenInterest]) VALUES (?,?,?,?);"""  %(_sqlTable_LME_precious_VolOpenInterest)
            params = (row[0], nameStr, row[1], row[2] )
            cursor.execute(query, params)              
        cnxn.commit()
        cursor.close()
        cnxn.close()    
    
# htmlFileFullPath = destFilePath =  constLME_a.commodityLME_workDir_A +'/2021-04-28/LME_gold.csv.html'
# nameStr = 'silver'
# sql_goldSilver_HTML_Price_Vol_OI(htmlFileFullPath)
# print()
        
def saveWebPage_nonFerrous_gold_Silver(url, destFilePath, destFileName, dateSearchBy, waitTime_loadWebsite): 
    driver = webdriver.Chrome('chromedriver.exe')
    driver.get(url)
    time.sleep(3)
    
    pyautogui.hotkey("f5")
    time.sleep(waitTime_loadWebsite)
    
    #-------get the date information
    date_field = driver.find_element_by_class_name(dateSearchBy)
    # print(date_field.text)
    time.sleep(3)    
        
    dateStr = date_field.text
    dateStr = dateSearch_LME(dateSearchBy, dateStr)
    
    # -------- make file dir, delete old file and set the file name   
    destFilePath_2 = destFilePath + '/' + dateStr  
    makeTodayDataDir(destFilePath_2)
    

    fileFullPath = destFilePath_2 + '/' + destFileName + '.html' 
    # fileFullPath = destFilePath_2 + '/' + destFileName
    if os.path.isfile(fileFullPath):
        os.remove(fileFullPath)
        print('file removed: ' + fileFullPath)
        time.sleep(5)
        
    #-----convert python dir to windows dir 
    fileAbsPath = os.path.abspath(fileFullPath)   
    winPath = fileAbsPath.replace(os.sep,ntpath.sep)
    
    pyautogui.hotkey('ctrl', 's')
    time.sleep(waitTime_loadWebsite)
    
    pyautogui.typewrite(winPath)
    time.sleep(2)
    
    pyautogui.hotkey('enter')
    time.sleep(waitTime_loadWebsite * 2) #wait for download finish
    
    driver.quit()    
    time.sleep(3)

    #check if the file is download with data
    fileSize = os.stat(fileFullPath).st_size
    if fileSize < 5000: # 5k
        msg = "website download data <10K: " + fileFullPath + " ; url: " + url 
        mydownPy.logError(errorFileTargetDir, msg)
    else: # save, update the data
        print('file donwloaded: ' + url)        
    return fileFullPath

# url =  constLME_a.DICT_URL_A.get(constLME_a.KEY_NONFERROUS)
# destFilePath =  constLME_a.commodityLME_workDir_A
# destFileName =  constLME_a.DICT_URL_A_FILENAME.get(constLME_a.KEY_NONFERROUS)
# dateSearchBy =  _dateSearchBy_ClassName_nonFerrous_gold_silver 
# waitTime_loadWebsite = _waitTime_loadWebsite_LME

# saveWebPage_nonFerrous_gold_Silver(url, destFilePath, destFileName, dateSearchBy, waitTime_loadWebsite) 
# print()

def update_DateFormat(df):         
    for i in range(len(df)): 
        yy = datetime.strptime(df.iat[i, 0], '%d %b %Y').strftime('%Y-%m-%d')
        df.iat[i, 0] = yy
    print()


def subFolders_toSql(sourceDir):
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
             
             # destFilePath =  constLME_a.commodityLME_workDir_A + '/workFolder'
             destFilePath =  constLME_a.commodityLME_workDir_A
             destFileName =  htmlFileName
             dateSearchBy =  _dateSearchBy_ClassName_nonFerrous_gold_silver 
             waitTime_loadWebsite = 1 
             
             # htmlFileFullPath = saveWebPage_nonFerrous_gold_Silver(url, destFilePath, destFileName, dateSearchBy, waitTime_loadWebsite) 

             if 'nonferrous' in htmlFileName.lower()  :
                htmlFileFullPath = saveWebPage_nonFerrous_gold_Silver(url, destFilePath, destFileName, dateSearchBy, waitTime_loadWebsite) 
 
                print('SQL: --' + htmlFileFullPath) 
                sql_NonFerrous_HTML_Stock_Price1(htmlFileFullPath)
                
             elif 'gold' in htmlFileName.lower() or 'silver' in htmlFileName.lower() :
                htmlFileFullPath = saveWebPage_nonFerrous_gold_Silver(url, destFilePath, destFileName, dateSearchBy, waitTime_loadWebsite) 
 
                sql_goldSilver_HTML_Price_Vol_OI(htmlFileFullPath)  
                
             else:
                # htmlFileFullPath = saveWebPage_nonFerrous_gold_Silver(url, destFilePath, destFileName, dateSearchBy, waitTime_loadWebsite) 
                # sql_NonFerrous_HTML_Stock_Price1(htmlFileFullPath)
                pass

# sourceDir = constLME_a.commodityLME_workDir_A+ '/workFolder'
# subFolders_toSql(sourceDir) 
# print()               

def daily_save_sql_webPages_nonFerrous_gold_Silver():  
    # url =  constLME_a.DICT_URL_A.get(constLME_a.KEY_NONFERROUS)
    destFilePath =  constLME_a.commodityLME_workDir_A
    # destFileName =  constLME_a.DICT_URL_A_FILENAME.get(constLME_a.KEY_NONFERROUS)
    dateSearchBy =  _dateSearchBy_ClassName_nonFerrous_gold_silver 
    waitTime_loadWebsite = _waitTime_loadWebsite_LME   

    for key, value in constLME_a.DICT_URL_A.items():
        url = value
        destFileName = constLME_a.DICT_URL_A_FILENAME.get(key)
        fileFullPath = saveWebPage_nonFerrous_gold_Silver(url, destFilePath, destFileName, dateSearchBy, waitTime_loadWebsite) 
        # print(fileFullPath)

        htmlFileFullPath = fileFullPath
        # htmlFileFullPath = destFilePath =  constLME_a.commodityLME_workDir_A +'/2021-04-28/London Metal Exchange_ Non-ferrous.html'
        
        if key == constLME_a.KEY_NONFERROUS :
            sql_NonFerrous_HTML_Stock_Price1(htmlFileFullPath)
            
        elif key == constLME_a.KEY_GOLD or key == constLME_a.KEY_SILVER :
            # htmlFileFullPath = constLME_a.commodityLME_workDir_A +'/2021-04-28/LME_gold.csv.html'
            # nameStr = 'silver'
            sql_goldSilver_HTML_Price_Vol_OI(htmlFileFullPath)            
        else:
            # sql_NonFerrous_HTML_Stock_Price1(htmlFileFullPath)
            pass
        
# daily_save_sql_webPages_nonFerrous_gold_Silver()
# print()



def LME_A_daily_Run():
    daily_save_sql_webPages_nonFerrous_gold_Silver()
    # saveAllwebPages_LME()       
    
# LME_daily_Run()
