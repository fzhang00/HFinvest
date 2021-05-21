# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 13:15:30 2021

http://www.kitconet.com/
# url = 'http://www.shfe.com.cn/statements/dataview.html?paramid=weeklystock' 
# url = '交易数据.html'

https://docs.microsoft.com/en-us/sql/machine-learning/data-exploration/python-dataframe-pandas?view=sql-server-ver15

@author: haoli

"""
# import pyodbc
# import pandas as pd
# # insert data from csv file into dataframe.
# # working directory for csv file: type "pwd" in Azure Data Studio or Linux
# # working directory in Windows c:\users\username
# df = pd.read_csv("c:\\user\\username\department.csv")
# # Some other example server values are
# # server = 'localhost\sqlexpress' # for a named instance
# # server = 'myserver,port' # to specify an alternate port
# server = 'yourservername' 
# database = 'AdventureWorks' 
# username = 'username' 
# password = 'yourpassword' 
# cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
# cursor = cnxn.cursor()
# # Insert Dataframe into SQL Server:
# for index, row in df.iterrows():
#     cursor.execute("INSERT INTO HumanResources.DepartmentTest (DepartmentID,Name,GroupName) values(?,?,?)", row.DepartmentID, row.Name, row.GroupName)
# cnxn.commit()
# cursor.close()


# import pyodbc
# import pandas as pd
# # Some other example server values are
# # server = 'localhost\sqlexpress' # for a named instance
# # server = 'myserver,port' # to specify an alternate port
# server = 'servername' 
# database = 'AdventureWorks' 
# username = 'yourusername' 
# password = 'databasename'  
# cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
# cursor = cnxn.cursor()
# # select 26 rows from SQL table to insert in dataframe.
# query = "SELECT [CountryRegionCode], [Name] FROM Person.CountryRegion;"
# df = pd.read_sql(query, cnxn)
# print(df.head(26))

# import requests

import Const_Shanghai_A as constSHFE

import sys
sys.path.append("../")
import const_common as constA
import downloadUpdateData as mydownPy

from os import makedirs
import os.path as myPath
import os

import pandas as pd
import pyodbc
import numpy as np

import pyautogui, time
pyautogui.PAUSE =2.5     #Set up a 2.5 second pause after each PyAutoGUI call:

from selenium import webdriver
import ntpath
# import glob
from pathlib import Path 
from datetime import datetime

#----------------------------------
errorFileTargetDir = '../'


dateSearchBy_ClassName_LME = "delayed-date.left"
dateSearchKeyword_LME = "Data valid for"
# waitTime_loadWebsite_LME = 3

waitTime_loadWebsite_SHFE = 6

_searchDateId_Weekly = "datatitle"
_stock_clinkID = 'weeklystock' #value = 'Weekly Market Data'
_volOI_clinkID = 'week' #value = 'Weekly Inventory'

# _stock_name = 'Weekly Market Data'
# _volOI_name = 'Weekly Inventory'

# mydownPy.logError("my test message")
#logError(errorFileTargetDir, msg)
# mydownPy.logError(errorFileTargetDir, "my test message")

# ------ Ryan's PC -----------
_server = 'RyanPC'
_database = 'Commodity_A1' 
_username = 'hl' 
_password = '123'        

_sqlTable_stock = 'SHFE_weeklyStock'
_sqlTable_priceVolOI = 'SHFE_weeklyPriceVolOI'

# ------ Fan's Laptop -------
# server = 'DESKTOP-45300G7'

def whitespace_remover(dataframe):
    for i in dataframe.columns:
        if dataframe[i].dtype == 'object': # applying strip function on column
            dataframe[i] = dataframe[i].map(str.strip)
        else: # if condn. is False then it will do nothing.
            pass
def makeTodayDataDir(newDir):
    # if not myPath.lexists(newDir): #lexists
    if not myPath.exists(newDir):
        makedirs(newDir)

def getDateFromString_SHFE(dateStr, keyword): 
    if keyword == '':
        d = dateStr
    else:        
        b = dateStr.split(keyword)
        d = b[1].strip()
        
    date_fromFile = d
    try:      
        date_fromFile = datetime.strptime(d, "%Y/%m/%d") #(d, "%m/%d/%Y") 
    except ValueError:
        try:
            date_fromFile = datetime.strptime(d, '%d %B %Y') # used LME
            # d.strftime("%A %d. %B %Y")
            # 'Monday 11. March 2002'
        except ValueError:
            try:
                date_fromFile = datetime.strptime(d, '%d %b %Y') # LME gold 01 Apr
            except ValueError:
                try:
                    # date_fromFile = datetime.strptime(d, '%Y年%m月%d日')  
                    date_fromFile = datetime.strptime(d, '%b.%d,%Y')  #Date:Mar.05,2021
                except ValueError:                
                    print('999 bad date conversion ' + d)
                    return d
    return date_fromFile.strftime('%Y-%m-%d')  

      
def save_updateData(mydf, toSave_csvFullpath1, toSave_csvFullpath2, toUpdate_csvFile):
    mydf.to_csv(toSave_csvFullpath1)
    mydf.to_csv(toSave_csvFullpath2)   
    try:        
        df_old = pd.read_csv(toUpdate_csvFile, index_col=['Date'])
        df_old.sort_index() #(inplace = True)
            #append to current working file            
        df_old = df_old.append(mydf)
        df1 = df_old[~df_old.index.duplicated(keep='last')] 
        
    except:
        print ('file did not exist for update: ' + toUpdate_csvFile)
        df1 = mydf
        # df1 = df_old[~df_old.index.duplicated(keep='last')] 
    # df1.sort_index()#(inplace = True)
    df1.to_csv(toUpdate_csvFile)        

def extract_SHFE_HTML_vol_OI_Weekly(htmlFileFullPath, workDataDir, appendDataDir):
    myDataFrameLists = pd.read_html(htmlFileFullPath)   
    if len(myDataFrameLists) == 0:
        msg = "empty table from website: " + htmlFileFullPath
        mydownPy.logError(errorFileTargetDir, msg)  
        return
    else: # DataFrame (3, 3)   
        htmlFilePath = constA.getFilePathInfo(htmlFileFullPath, 0) #/temp/2021-04-01
        date_fromFolderName  = constA.getFilePathInfo(htmlFilePath, 1) #2021-04-01      

        for df in myDataFrameLists:
            # df.iloc[0,0].str.contains(r'TOTAL PLEDGED', case = False, na= False):
            if "Species:cu" == (str(df.iloc[1,0])):
                df_cu = [{'Date': date_fromFolderName,
                          constSHFE.SHFE_OIVolCol1 : df.iloc[-1,6],
                          constSHFE.SHFE_OIVolCol2 : df.iloc[-1,9],
                          constSHFE.SHFE_OIVolCol3 : df.iloc[-1,10]} ] #total money exchanged
                mydf = pd.DataFrame(df_cu)                
                csvFileName = constSHFE.SH_openInterestVolumn_FileName_disct.get(constSHFE.cuKey)
                
            elif "Species:bc" == (str(df.iloc[1,0])):     
                df_cuBC = [{'Date': date_fromFolderName,
                          constSHFE.SHFE_OIVolCol1 : df.iloc[-1,6],
                          constSHFE.SHFE_OIVolCol2 : df.iloc[-1,9],
                          constSHFE.SHFE_OIVolCol3 : df.iloc[-1,10]} ] #total money exchanged 
                mydf = pd.DataFrame(df_cuBC)
                csvFileName = constSHFE.SH_openInterestVolumn_FileName_disct.get(constSHFE.cuBCKey)
                
            elif "Species:al" == (str(df.iloc[1,0])):
                df_AL = [{'Date': date_fromFolderName,
                          constSHFE.SHFE_OIVolCol1 : df.iloc[-1,6],
                          constSHFE.SHFE_OIVolCol2 : df.iloc[-1,9],
                          constSHFE.SHFE_OIVolCol3 : df.iloc[-1,10]} ] #total money exchanged
                mydf = pd.DataFrame(df_AL)
                csvFileName = constSHFE.SH_openInterestVolumn_FileName_disct.get(constSHFE.alKey)
                
            elif "Species:zn" == (str(df.iloc[1,0])):
                df_Zn  = [{'Date': date_fromFolderName,
                          constSHFE.SHFE_OIVolCol1 : df.iloc[-1,6],
                          constSHFE.SHFE_OIVolCol2 : df.iloc[-1,9],
                          constSHFE.SHFE_OIVolCol3 : df.iloc[-1,10]} ] #total money exchanged  
                mydf = pd.DataFrame(df_Zn)
                csvFileName = constSHFE.SH_openInterestVolumn_FileName_disct.get(constSHFE.znKey)
                
            elif "Species:pb" == (str(df.iloc[1,0])): 
                df_Pb = [{'Date': date_fromFolderName,
                          constSHFE.SHFE_OIVolCol1 : df.iloc[-1,6],
                          constSHFE.SHFE_OIVolCol2 : df.iloc[-1,9],
                          constSHFE.SHFE_OIVolCol3 : df.iloc[-1,10]} ] #total money exchanged 
                mydf = pd.DataFrame(df_Pb)
                csvFileName = constSHFE.SH_openInterestVolumn_FileName_disct.get(constSHFE.pbKey)
                
            elif "Species:ni" == (str(df.iloc[1,0])):
                df_Ni = [{'Date': date_fromFolderName,
                          constSHFE.SHFE_OIVolCol1 : df.iloc[-1,6],
                          constSHFE.SHFE_OIVolCol2 : df.iloc[-1,9],
                          constSHFE.SHFE_OIVolCol3 : df.iloc[-1,10]} ] #total money exchanged    
                mydf = pd.DataFrame(df_Ni)
                csvFileName = constSHFE.SH_openInterestVolumn_FileName_disct.get(constSHFE.niKey)
                
            elif "Species:sn" == (str(df.iloc[1,0])):
                df_Tin = [{'Date': date_fromFolderName,
                          constSHFE.SHFE_OIVolCol1 : df.iloc[-1,6],
                          constSHFE.SHFE_OIVolCol2 : df.iloc[-1,9],
                          constSHFE.SHFE_OIVolCol3 : df.iloc[-1,10]} ] #total money exchanged  
                mydf = pd.DataFrame(df_Tin)
                csvFileName = constSHFE.SH_openInterestVolumn_FileName_disct.get(constSHFE.tinKey)
                
            elif "Species:au" == (str(df.iloc[1,0])):
                df_Gold = [{'Date': date_fromFolderName,
                          constSHFE.SHFE_OIVolCol1 : df.iloc[-1,6],
                          constSHFE.SHFE_OIVolCol2 : df.iloc[-1,9],
                          constSHFE.SHFE_OIVolCol3 : df.iloc[-1,10]} ] #total money exchanged
                mydf = pd.DataFrame(df_Gold)
                csvFileName = constSHFE.SH_openInterestVolumn_FileName_disct.get(constSHFE.goldKey)
                
            elif "Species:ag" == (str(df.iloc[1,0])):
                df_Silver = [{'Date': date_fromFolderName,
                          constSHFE.SHFE_OIVolCol1 : df.iloc[-1,6],
                          constSHFE.SHFE_OIVolCol2 : df.iloc[-1,9],
                          constSHFE.SHFE_OIVolCol3 : df.iloc[-1,10]} ] #total money exchanged  
                mydf = pd.DataFrame(df_Silver)
                csvFileName = constSHFE.SH_openInterestVolumn_FileName_disct.get(constSHFE.silverKey)
                
            else:
                mydf = pd.DataFrame()
                csvFileName = "notfound"
            
            if mydf.empty: 
                pass
            else:
                toSave_csvFullpath1 = htmlFilePath + '/' + csvFileName
                toSave_csvFullpath2 = workDataDir + '/' + csvFileName
                toUpdate_csvFile    = appendDataDir + '/' + csvFileName                    
       
                mydf.set_index('Date', inplace = True)    
                save_updateData(mydf,toSave_csvFullpath1, toSave_csvFullpath2, toUpdate_csvFile)


# htmlFileFullPath = constSHFE.commodityShanghai_dataDir_OIVolPrice + '/2021-03-05/Shanghai_OpenInterest_Volumn_weekly.csv.html'

# workDataDir     = constSHFE.commodityShanghai_dataDir_OIVolPrice
# appendDataDir   = constSHFE.commodityShanghaiDir_OIVolPrice 

# extract_SHFE_HTML_vol_OI_Weekly(htmlFileFullPath, workDataDir, appendDataDir)
# print()

def sql_SHFE_OIVol_Weekly(htmlFileFullPath): #, workDataDir, appendDataDir):   
    try:      
        myDataFrameLists = pd.read_html(htmlFileFullPath) 
    except ValueError:
        print ("error to read html file: " + htmlFileFullPath)
        return   
    if len(myDataFrameLists) == 0:
        msg = "empty table from website: " + htmlFileFullPath
        mydownPy.logError(errorFileTargetDir, msg)  
        return
    else: # DataFrame (3, 3)    

        htmlFilePath = constA.getFilePathInfo(htmlFileFullPath, 0) #/temp/2021-04-01
        date_fromFolderName  = constA.getFilePathInfo(htmlFilePath, 1) #2021-04-01        
            
        #--------sql connection 
        # Make connection and get cursor
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server+';DATABASE='+_database+';UID='+_username+';PWD='+_password)
        cursor = cnxn.cursor()
        
        query = """DELETE FROM %s where Date = '%s';""" % (_sqlTable_priceVolOI, date_fromFolderName)
        cursor.execute(query)        
        
        query = """INSERT INTO %s ([Date],Species,[Open],[High],[Low],[Close], PriceDif,OpenInterest,OIDif,PostPrice,Volume,TurnOver) VALUES (?,?,?,?, ?,?,?,?, ?,?,?,? );""" %(_sqlTable_priceVolOI)
                
        for df in myDataFrameLists:
            # df.iloc[0,0].str.contains(r'TOTAL PLEDGED', case = False, na= False):
            df = df.replace({np.NAN: None}) 
            # whitespace_remover(df)
            for row in df.itertuples():
                firstCell = str(row[1])
                # print(firstCell)
                if ("species" in firstCell.lower()) or \
                    ("total" in firstCell.lower()) or \
                    ("note" in firstCell.lower()):
                    pass
                elif 'SHFE Nonferrous Metals Index' in firstCell :
                    params = [date_fromFolderName, 'Index_Nonferrous', row[2], row[3], row[4], row[5], row[6],\
                               None, None, None, None, None]
                    # print(params)
                    cursor.execute(query, params)                                  
                elif (  ("cu" in firstCell.lower()) or 
                        ("bc" in firstCell.lower()) or 
                        ("al" in firstCell.lower()) or 
                        ("zn" in firstCell.lower()) or 
                        ("pb" in firstCell.lower()) or 
                        ("ni" in firstCell.lower()) or 
                        ("sn" in firstCell.lower()) or 
                        ("au" in firstCell.lower()) or 
                        ("ag" in firstCell.lower()) ): 
                    
                    params = [date_fromFolderName, row[1], row[2], row[3], row[4], \
                              row[5], row[6], row[7], row[8], row[9], row[10], row[11]]
                    # print(params)
                    cursor.execute(query, params)                             
        #commit and close     
        cnxn.commit()
        cursor.close()
        cnxn.close()
        
# htmlFileFullPath = constSHFE.commodityShanghai_dataDir_OIVolPrice + '/2021-03-07/Shanghai_OpenInterest_Volumn_weekly.csv.html'
# sql_SHFE_OIVol_Weekly(htmlFileFullPath)
# print()

def saveWebPage_SHFE_OIVolPrice_weekly(url, filePath, volPriceFileName, dateSearchBy, searchKeyword, waitTime_loadWebsite): 
    # driver = webdriver.Chrome('chromedriver.exe')
    driver = webdriver.Chrome('chromedriver.exe')  # Optional argument, if not specified will search path.
    driver.get(url)
    #refresh the webpage first
    time.sleep(1)
    pyautogui.hotkey("f5")   
    time.sleep(waitTime_loadWebsite)  
    
    driver.find_element_by_id(_volOI_clinkID).click()
    time.sleep(waitTime_loadWebsite * 3)
    
    #-------get the date information
    date_field = driver.find_element_by_id(dateSearchBy)
    time.sleep(3)
  
    dateStr1 = (date_field.text).splitlines()
    dateStr2 = dateStr1[1]   #---------- 
    keyword = searchKeyword
    dateStr = getDateFromString_SHFE(dateStr2, keyword)
    # -------- make file dir, delete old file and set the file name
    filePath_new = filePath + '/' + dateStr  
    makeTodayDataDir(filePath_new)  
    
#-----repeat the code for anohter page -
    fileFullPath_stock = filePath_new + '/' + volPriceFileName + '.html'  
    if os.path.isfile(fileFullPath_stock):
        os.remove(fileFullPath_stock)
        print('file removed: ' + fileFullPath_stock)
        time.sleep(5)        
    #-----convert python dir to windows dir 
    fileAbsPath = os.path.abspath(fileFullPath_stock)   
    winPath = fileAbsPath.replace(os.sep,ntpath.sep)    
    #-----Save the website using windows command
    pyautogui.hotkey('ctrl', 's')
    # Wait for the Save As dialog to load. Might need to increase the wait time on slower machines
    time.sleep(waitTime_loadWebsite)
    
    # Type the file path and name is Save AS dialog
    pyautogui.typewrite(winPath)
    time.sleep(3)
    
    #Hit Enter to save
    pyautogui.hotkey('enter')
    time.sleep(waitTime_loadWebsite * 2) #wait for download finish
    
    driver.quit()
    time.sleep(1)
    
    #check if the file is download with data
    fileSize = os.stat(fileFullPath_stock).st_size
    if fileSize < 5000: # 5k
        msg = "website download data <10K: " + fileFullPath_stock + " ; url: " + url 
        mydownPy.logError(errorFileTargetDir, msg)
    else: # save, update the data
        print('file donwloaded: ' + url)         
        
        htmlFileFullPath = fileFullPath_stock
        # htmlFileFullPath = constSHFE.commodityShanghai_dataDir_OIVolPrice + '/2021-03-05/Shanghai_OpenInterest_Volumn_weekly.csv.html'
        workDataDir     = constSHFE.commodityShanghai_dataDir_OIVolPrice
        appendDataDir   = constSHFE.commodityShanghaiDir_OIVolPrice 
        
        extract_SHFE_HTML_vol_OI_Weekly(htmlFileFullPath, workDataDir, appendDataDir)
        
        # # database update
        # sql_SHFE_OIVol_Weekly(htmlFileFullPath)

    return htmlFileFullPath


# fileFullPath = constSHFE.commodityShanghai_dataDir_OIVolPrice + '/2021-03-05/Shanghai_OpenInterest_Volumn_weekly.csv.html'
# fileAbsPath = os.path.abspath(fileFullPath)   
# winPath = fileAbsPath.replace(os.sep,ntpath.sep)
# url = winPath
# url = constSHFE.SHStock_url_weekly

# filePath = constSHFE.commodityShanghai_dataDir_OIVolPrice  
# volPriceFileName = constSHFE.SH_openInterest_Vol_fileName_weekly   
# dateSearchBy = _searchDateId_Weekly
# searchKeyword = '--'
# waitTime_loadWebsite = 3
# dateStr = saveWebPage_SHFE_OIVolPrice_weekly(url, filePath, stockFileName, dateSearchBy, searchKeyword, waitTime_loadWebsite)
# print(dateStr)

def extract_SHFE_HTML_StockWeekly(htmlFileFullPath, workDataDir, appendDataDir):   
    myDataFrameLists = pd.read_html(htmlFileFullPath)   
    if len(myDataFrameLists) == 0:
        msg = "empty table from website: " + htmlFileFullPath
        mydownPy.logError(errorFileTargetDir, msg)  
        return
    else: # DataFrame (3, 3)  
        htmlFilePath = constA.getFilePathInfo(htmlFileFullPath, 0) #/temp/2021-04-01
        date_fromFolderName  = constA.getFilePathInfo(htmlFilePath, 1) #2021-04-01        

        for df in myDataFrameLists:
            # df.iloc[0,0].str.contains(r'TOTAL PLEDGED', case = False, na= False):
            if "copper" == (str(df.iloc[0,0]).lower()):
                df_cu = [{'Date': date_fromFolderName,
                          constSHFE.SHFE_StockCol2 :  df.iloc[-1,4],
                          constSHFE.SHFE_StockCol1 : df.iloc[-1,5]} ]
                mydf = pd.DataFrame(df_cu)
                csvFileName = constSHFE.SH_stockFileName_disct.get(constSHFE.cuKey)
                
            elif "copper(bc)" == (str(df.iloc[0,0]).lower()):     
                df_cuBC = [{'Date': date_fromFolderName,
                            constSHFE.SHFE_StockCol2 :  df.iloc[-2,4],
                            constSHFE.SHFE_StockCol1 : df.iloc[-2,5]} ] 
                mydf = pd.DataFrame(df_cuBC)
                csvFileName = constSHFE.SH_stockFileName_disct.get(constSHFE.cuBCKey)
                
            elif "aluminium" == (str(df.iloc[0,0]).lower()):
                df_AL = [{'Date': date_fromFolderName,
                          constSHFE.SHFE_StockCol2 :  df.iloc[-1,4],
                          constSHFE.SHFE_StockCol1 : df.iloc[-1,5]} ]
                mydf = pd.DataFrame(df_AL)
                csvFileName = constSHFE.SH_stockFileName_disct.get(constSHFE.alKey)
                
            elif "zinc" == (str(df.iloc[0,0]).lower()):
                df_Zn  = [{'Date': date_fromFolderName,
                          constSHFE.SHFE_StockCol2 :  df.iloc[-1,4],
                          constSHFE.SHFE_StockCol1 : df.iloc[-1,5]} ] 
                mydf = pd.DataFrame(df_Zn)
                csvFileName = constSHFE.SH_stockFileName_disct.get(constSHFE.znKey)
                
            elif "lead" == (str(df.iloc[0,0]).lower()): 
                df_Pb = [{'Date': date_fromFolderName,
                          constSHFE.SHFE_StockCol2 :  df.iloc[-1,4],
                          constSHFE.SHFE_StockCol1 : df.iloc[-1,5]} ] 
                mydf = pd.DataFrame(df_Pb)
                csvFileName = constSHFE.SH_stockFileName_disct.get(constSHFE.pbKey)
                
            elif "nickel" == (str(df.iloc[0,0]).lower()):
                df_Ni = [{'Date': date_fromFolderName,
                          constSHFE.SHFE_StockCol2 :  df.iloc[-1,4],
                          constSHFE.SHFE_StockCol1 : df.iloc[-1,5]} ] 
                mydf = pd.DataFrame(df_Ni)
                csvFileName = constSHFE.SH_stockFileName_disct.get(constSHFE.niKey)
                
            elif "tin" == (str(df.iloc[0,0]).lower()):
                df_Tin = [{'Date': date_fromFolderName,
                          constSHFE.SHFE_StockCol2 :  df.iloc[-1,4],
                          constSHFE.SHFE_StockCol1 : df.iloc[-1,5]} ]
                mydf = pd.DataFrame(df_Tin)
                csvFileName = constSHFE.SH_stockFileName_disct.get(constSHFE.tinKey)
                
            elif "gold" == (str(df.iloc[0,0]).lower()):
                df_Gold = [{'Date': date_fromFolderName,
                          constSHFE.SHFE_StockCol1 :  df.iloc[-1,1] } ]
                mydf = pd.DataFrame(df_Gold)
                csvFileName = constSHFE.SH_stockFileName_disct.get(constSHFE.goldKey)
                
            elif "silver" == (str(df.iloc[0,0]).lower()):
                df_Silver = [{'Date': date_fromFolderName,
                          constSHFE.SHFE_StockCol1 :  df.iloc[-1,3] }] 
                mydf = pd.DataFrame(df_Silver)
                csvFileName = constSHFE.SH_stockFileName_disct.get(constSHFE.silverKey)
                
            else:
                mydf = pd.DataFrame()
                csvFileName = "notfound"
            
            if mydf.empty: 
                pass
            else:
                toSave_csvFullpath1 = htmlFilePath + '/' + csvFileName
                toSave_csvFullpath2 = workDataDir + '/' + csvFileName
                toUpdate_csvFile    = appendDataDir + '/' + csvFileName                    
       
                mydf.set_index('Date', inplace = True)    
                save_updateData(mydf,toSave_csvFullpath1, toSave_csvFullpath2, toUpdate_csvFile)

#-------------
# htmlFileFullPath = constSHFE.commodityShanghai_dataDir + '/2021-04-16/ShanghaiStock_weekly.csv.html'
# workDataDir     = constSHFE.commodityShanghai_dataDir
# appendDataDir   = constSHFE.commodityShanghaiDir 
# extract_SHFE_HTML_StockWeekly(htmlFileFullPath, workDataDir, appendDataDir)

        
def sql_SHFE_StockWeekly(htmlFileFullPath): #, workDataDir, appendDataDir):   
    try:      
        myDataFrameLists = pd.read_html(htmlFileFullPath) 
    except ValueError:
        print ("error to read html file: " + htmlFileFullPath)
        return
      
    if len(myDataFrameLists) == 0:
        msg = "empty table from website: " + htmlFileFullPath
        mydownPy.logError(errorFileTargetDir, msg)  
        return
    else: # DataFrame (3, 3)    

        htmlFilePath = constA.getFilePathInfo(htmlFileFullPath, 0) #/temp/2021-04-01
        date_fromFolderName  = constA.getFilePathInfo(htmlFilePath, 1) #2021-04-01        
            
        #--------sql connection 
        # Make connection and get cursor
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server+';DATABASE='+_database+';UID='+_username+';PWD='+_password)
        cursor = cnxn.cursor()
        
        query = """DELETE FROM %s where Date = '%s';""" % (_sqlTable_stock, date_fromFolderName)
        cursor.execute(query)        
        query = """INSERT INTO %s (Date, Future, OnWarrant, Deliverable) VALUES (?,?,?,?);""" %(_sqlTable_stock)
        # params = [date_fromFolderName, 'Al',1011, None]
        # cursor.execute(query, params)
        for df in myDataFrameLists:
            # df.iloc[0,0].str.contains(r'TOTAL PLEDGED', case = False, na= False):
            # whitespace_remover(df)    
            if "copper" == (str(df.iloc[0,0]).lower()):
                params = [date_fromFolderName, 'cu',    df.iloc[-1,5], df.iloc[-1,4]]
                cursor.execute(query, params)
                
            elif "copper(bc)" == (str(df.iloc[0,0]).lower()):     
                params = [date_fromFolderName, 'bc',  df.iloc[-2,5], df.iloc[-2,4]]
                cursor.execute(query, params) 
                
            elif "aluminium" == (str(df.iloc[0,0]).lower()):
                params = [date_fromFolderName, 'al',    df.iloc[-1,5], df.iloc[-1,4]]
                cursor.execute(query, params)
                
            elif "zinc" == (str(df.iloc[0,0]).lower()):
                params = [date_fromFolderName, 'zn',    df.iloc[-1,5], df.iloc[-1,4]]
                cursor.execute(query, params)
                
            elif "lead" == (str(df.iloc[0,0]).lower()):   
                params = [date_fromFolderName, 'pb',    df.iloc[-1,5], df.iloc[-1,4]]
                cursor.execute(query, params)
                
            elif "nickel" == (str(df.iloc[0,0]).lower()):
                params = [date_fromFolderName, 'ni',    df.iloc[-1,5], df.iloc[-1,4]]
                cursor.execute(query, params)
                
            elif "tin" == (str(df.iloc[0,0]).lower()):
                params = [date_fromFolderName, 'sn',    df.iloc[-1,5], df.iloc[-1,4]]
                cursor.execute(query, params)
                
            elif "gold" == (str(df.iloc[0,0]).lower()):
                params = [date_fromFolderName, 'au', df.iloc[-1,1], None]
                cursor.execute(query, params)
                
            elif "silver" == (str(df.iloc[0,0]).lower()):
                params = [date_fromFolderName, 'ag', df.iloc[-1,3], None]
                cursor.execute(query, params)
        
        #commit and close     
        cnxn.commit()
        cursor.close()
        cnxn.close()

# htmlFileFullPath = constSHFE.commodityShanghai_dataDir + '/2021-04-30/ShanghaiStock_weekly.csv.html'
# sql_SHFE_StockWeekly(htmlFileFullPath)
# print()    
"""
return the folder dir for the weekly SHFE data
"""    
def saveWebPageShangHai_weeklyStock(url, filePath, stockFileName, dateSearchBy, searchKeyword, waitTime_loadWebsite): 
    # driver = webdriver.Chrome('chromedriver.exe')
    driver = webdriver.Chrome('chromedriver.exe')  # Optional argument, if not specified will search path.
    driver.get(url)
    #refresh the webpage first
    time.sleep(1)
    pyautogui.hotkey("f5")   
    time.sleep(waitTime_loadWebsite)  
    
    driver.find_element_by_id(_stock_clinkID).click()
    time.sleep(waitTime_loadWebsite * 3)
    
    #-------get the date information
    date_field = driver.find_element_by_id(dateSearchBy)
    time.sleep(3)
  
    dateStr1 = (date_field.text).splitlines()
    dateStr2 = dateStr1[2]    
    keyword = searchKeyword
    dateStr = getDateFromString_SHFE(dateStr2, keyword)
    
    # -------- make file dir, delete old file and set the file name
    # filePath_2 = filePath + '\\' + dateStr     
    filePath_new = filePath + '/' + dateStr  
    makeTodayDataDir(filePath_new)    
    # print(os.getcwd() ) 
    
#-----repeat the code for anohter page -
    fileFullPath_stock = filePath_new + '/' + stockFileName + '.html'  
    if os.path.isfile(fileFullPath_stock):
        os.remove(fileFullPath_stock)
        print('file removed: ' + fileFullPath_stock)
        time.sleep(5)        
    #-----convert python dir to windows dir 
    fileAbsPath = os.path.abspath(fileFullPath_stock)   
    winPath = fileAbsPath.replace(os.sep,ntpath.sep)    
    #-----Save the website using windows command
    pyautogui.hotkey('ctrl', 's')
    # Wait for the Save As dialog to load. Might need to increase the wait time on slower machines
    time.sleep(waitTime_loadWebsite)
    
    # Type the file path and name is Save AS dialog
    pyautogui.typewrite(winPath)
    time.sleep(3)
    
    #Hit Enter to save
    pyautogui.hotkey('enter')
    time.sleep(waitTime_loadWebsite * 2) #wait for download finish
    
    driver.quit()
    time.sleep(1)
    
    #check if the file is download with data
    fileSize = os.stat(fileFullPath_stock).st_size
    if fileSize < 5000: # 5k
        msg = "website download data <10K: " + fileFullPath_stock + " ; url: " + url 
        mydownPy.logError(errorFileTargetDir, msg)
    else: # save, update the data
        print('file donwloaded: ' + url)        
        
        htmlFileFullPath = fileFullPath_stock      
        # htmlFileFullPath = constSHFE.commodityShanghai_dataDir + '/2021-04-16/ShanghaiStock_weekly.csv.html'
        workDataDir     = constSHFE.commodityShanghai_dataDir
        appendDataDir   = constSHFE.commodityShanghaiDir 
        
        extract_SHFE_HTML_StockWeekly(htmlFileFullPath, workDataDir, appendDataDir)
        
    return htmlFileFullPath


def sql_SHFE_Stock_all_subFolders(sourceDir):
    pathlist = Path(sourceDir).glob('**/*.html')
    for path in pathlist:
         # because path is object not string
         htmlFileFullPath = str(path)
         
         if 'saved_resource' in htmlFileFullPath: # there is saved_resource.html in the folder
             pass
         else:
             fileAbsPath = os.path.abspath(htmlFileFullPath)   
             winPath = fileAbsPath.replace(os.sep,ntpath.sep)
             url = winPath
             print (url)
             filePath = constSHFE.commodityShanghai_dataDir    
             stockFileName = constSHFE.SHStockfileName_weekly    
             dateSearchBy = _searchDateId_Weekly
             searchKeyword = ':'
             waitTime_loadWebsite = 1
             
             htmlFileFullPath = saveWebPageShangHai_weeklyStock(url, filePath, stockFileName, dateSearchBy, searchKeyword, waitTime_loadWebsite)
                        
             #load to sql
             # htmlFileFullPath = constSHFE.commodityShanghai_dataDir + '/' + date_StockDownload             
             print(htmlFileFullPath)
             sql_SHFE_StockWeekly(htmlFileFullPath)               
         
# sourceDir = constSHFE.commodityShanghai_dataDir  
# # sourceDir = constSHFE.commodityShanghai_dataDir + '/2021-0102'      
# sql_SHFE_Stock_all_subFolders(sourceDir)         

# htmlFileFullPath = constSHFE.commodityShanghai_dataDir + '/2020/55ShanghaiStock_weekly.csv.html'
# sql_SHFE_StockWeekly(htmlFileFullPath)

def sql_SHFE_OIvol_all_subFolders(sourceDir):
    pathlist = Path(sourceDir).glob('**/*.html')
    for path in pathlist:
         # because path is object not string
         htmlFileFullPath = str(path)
         
         if 'saved_resource' in htmlFileFullPath: # there is saved_resource.html in the folder
             pass
         else:
             fileAbsPath = os.path.abspath(htmlFileFullPath)   
             winPath = fileAbsPath.replace(os.sep,ntpath.sep)
             url = winPath
             print (url)
             
             filePath = constSHFE.commodityShanghai_dataDir_OIVolPrice  
             stockFileName = constSHFE.SH_openInterest_Vol_fileName_weekly   
             dateSearchBy = _searchDateId_Weekly
             searchKeyword = '--'
             waitTime_loadWebsite = 1
            
             htmlFileFullPath = saveWebPage_SHFE_OIVolPrice_weekly(url, filePath, stockFileName, dateSearchBy, searchKeyword, waitTime_loadWebsite)

             #load to sql
             # htmlFileFullPath = constSHFE.commodityShanghai_dataDir_OIVolPrice + '/' + date_OIDownload
             print(htmlFileFullPath)
             sql_SHFE_OIVol_Weekly(htmlFileFullPath) 
            

# sourceDir = constSHFE.commodityShanghai_dataDir_OIVolPrice 
# # sourceDir = constSHFE.commodityShanghai_dataDir_OIVolPrice + '/backup'      
# sql_SHFE_OIvol_all_subFolders(sourceDir)
# print()        



#----------------------------------------------
def weeklyRun_SHFE_Stock():         
    url = constSHFE.SHStock_url_weekly    
    filePath = constSHFE.commodityShanghai_dataDir    
    stockFileName = constSHFE.SHStockfileName_weekly    
    dateSearchBy = _searchDateId_Weekly
    searchKeyword = ':'
    waitTime_loadWebsite = waitTime_loadWebsite_SHFE
    
    date_StockDownload_1 = saveWebPageShangHai_weeklyStock(url, filePath, stockFileName, dateSearchBy, searchKeyword, waitTime_loadWebsite)
    
   
    #-----------------process OI vol and price    
    url = constSHFE.SHStock_url_weekly
    filePath = constSHFE.commodityShanghai_dataDir_OIVolPrice
    volPriceFileName = constSHFE.SH_openInterest_Vol_fileName_weekly 
    dateSearchBy = _searchDateId_Weekly
    searchKeyword = '--'
    waitTime_loadWebsite = waitTime_loadWebsite_SHFE    

    date_OIDownload_2 = saveWebPage_SHFE_OIVolPrice_weekly(url, filePath, volPriceFileName, dateSearchBy, searchKeyword, waitTime_loadWebsite)
    
    #load to sql
    print("insert to SQL: " + date_StockDownload_1)   
    sql_SHFE_StockWeekly(date_StockDownload_1)  
    
    #load to sql
    print("insert to SQL: " + date_OIDownload_2)
    sql_SHFE_OIVol_Weekly(date_OIDownload_2)     

# weeklyRun_SHFE_Stock()


"""
not userd
"""
#-----------not used-----
def backup_saveWebPage_SHFE_OIVolPrice_weekly(url, elementID_click, filePath, fileName, waitTime_loadWebsite): 
                                        # (url, filePath, stockFileName, dateSearchBy, searchKeyword, waitTime_loadWebsite):
    driver = webdriver.Chrome('chromedriver.exe')  # Optional argument, if not specified will search path.
    driver.get(url)
    time.sleep(1)
    pyautogui.hotkey("f5")   
    time.sleep(waitTime_loadWebsite * 2)  
    
    driver.find_element_by_id(elementID_click).click()
    time.sleep(waitTime_loadWebsite * 2)

    # #-------get the date information
    # date_field = driver.find_element_by_id(dateSearchBy)
    # time.sleep(3)
  
    # dateStr1 = (date_field.text).splitlines()
    # dateStr2 = dateStr1[2]    
    # keyword = searchKeyword
    # dateStr = getDateFromString_SHFE(dateStr2, keyword)    


    # -------- make file dir, delete old file and set the file name
    makeTodayDataDir(filePath)     
#-----repeat the code for anohter page -
    fileFullPath = filePath + '/' + fileName + '.html'  
    if os.path.isfile(fileFullPath):
        os.remove(fileFullPath)
        print('file removed: ' + fileFullPath)
        time.sleep(5)        
    #-----convert python dir to windows dir 
    fileAbsPath = os.path.abspath(fileFullPath)   
    winPath = fileAbsPath.replace(os.sep,ntpath.sep)    
    #-----Save the website using windows command
    pyautogui.hotkey('ctrl', 's')
    time.sleep(waitTime_loadWebsite)
    
    pyautogui.typewrite(winPath)
    time.sleep(3)
    
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
        
        htmlFileFullPath = fileFullPath      
        # htmlFileFullPath = constSHFE.commodityShanghai_dataDir + '/2021-04-16/ShanghaiStock_weekly.csv.html'
        workDataDir     = constSHFE.commodityShanghaiDir_OIVolPrice
        appendDataDir   = constSHFE.commodityShanghai_dataDir_OIVolPrice
      
        extract_SHFE_HTML_vol_OI_Weekly(htmlFileFullPath, workDataDir, appendDataDir)


# url = constSHFE.SHStock_url_weekly
# elementID_click = _volOI_clinkID

# filePath = constSHFE.commodityShanghai_dataDir + '/2021-04-16' #constSHFE.commodityShanghai_dataDir

# fileName = constSHFE.commodityShanghai_dataDir_OIVolPrice
# waitTime_loadWebsite = waitTime_loadWebsite_SHFE

# saveWebPage_SHFE_OIVolPrice_weekly(url, elementID_click, filePath, fileName, waitTime_loadWebsite)       



def NotUsed_saveWebPageShangHai_weeklyStock_backup(url, filePath, stockFileName, dateSearchBy, searchKeyword, waitTime_loadWebsite): 
    # driver = webdriver.Chrome('chromedriver.exe')
    driver = webdriver.Chrome('chromedriver.exe')  # Optional argument, if not specified will search path.
    driver.get(url)
    #refresh the webpage first
    time.sleep(1)
    pyautogui.hotkey("f5")   
    time.sleep(waitTime_loadWebsite)  
    
    driver.find_element_by_id(_stock_clinkID).click()
    time.sleep(waitTime_loadWebsite * 3)
    
    #-------get the date information
    date_field = driver.find_element_by_id(dateSearchBy)
    time.sleep(3)
  
    dateStr1 = (date_field.text).splitlines()
    dateStr2 = dateStr1[2]    
    keyword = searchKeyword
    dateStr = getDateFromString_SHFE(dateStr2, keyword)
    
    # -------- make file dir, delete old file and set the file name
    # filePath_2 = filePath + '\\' + dateStr     
    filePath_new = filePath + '/' + dateStr  
    makeTodayDataDir(filePath_new)    
    # print(os.getcwd() ) 
    
#-----repeat the code for anohter page -
    fileFullPath_stock = filePath_new + '/' + stockFileName + '.html'  
    if os.path.isfile(fileFullPath_stock):
        os.remove(fileFullPath_stock)
        print('file removed: ' + fileFullPath_stock)
        time.sleep(5)        
    #-----convert python dir to windows dir 
    fileAbsPath = os.path.abspath(fileFullPath_stock)   
    winPath = fileAbsPath.replace(os.sep,ntpath.sep)    
    #-----Save the website using windows command
    pyautogui.hotkey('ctrl', 's')
    # Wait for the Save As dialog to load. Might need to increase the wait time on slower machines
    time.sleep(waitTime_loadWebsite)
    
    # Type the file path and name is Save AS dialog
    pyautogui.typewrite(winPath)
    time.sleep(3)
    
    #Hit Enter to save
    pyautogui.hotkey('enter')
    time.sleep(waitTime_loadWebsite * 2) #wait for download finish
    
    driver.quit()
    time.sleep(3)
    
    #check if the file is download with data
    fileSize = os.stat(fileFullPath_stock).st_size
    if fileSize < 5000: # 5k
        msg = "website download data <10K: " + fileFullPath_stock + " ; url: " + url 
        mydownPy.logError(errorFileTargetDir, msg)
    else: # save, update the data
        print('file donwloaded: ' + url)        
        
        htmlFileFullPath = fileFullPath_stock      
        # htmlFileFullPath = constSHFE.commodityShanghai_dataDir + '/2021-04-16/ShanghaiStock_weekly.csv.html'
        workDataDir     = constSHFE.commodityShanghai_dataDir
        appendDataDir   = constSHFE.commodityShanghaiDir 
        
        extract_SHFE_HTML_StockWeekly(htmlFileFullPath, workDataDir, appendDataDir)
        
    return dateStr
