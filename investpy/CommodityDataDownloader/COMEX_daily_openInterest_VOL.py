# -*- coding: utf-8 -*-
"""

https://docs.microsoft.com/en-us/sql/machine-learning/data-exploration/python-dataframe-pandas?view=sql-server-ver15

@author: haoli

"""


import sys
sys.path.append("../")

import const_common as constA
import downloadUpdateData as mydownPy
import Const_NYMEXCOMEX_A as constCOMEX_A


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

from urllib.request import urlopen, Request

#----------------------------------
errorFileTargetDir = '../'
pd.set_option('mode.chained_assignment', None)

# mydownPy.logError("my test message")
#logError(errorFileTargetDir, msg)
# mydownPy.logError(errorFileTargetDir, "my test message")
# ------ Ryan's PC -----------
_server = 'RyanPC'
_database = 'Commodity_A1' 
_username = 'hl' 
_password = '123'     

#--------table name ---------
_sqlTable_COMEX_Daily_Vol_OpenInterest_Agriculture      = 'COMEX_Daily_Volume_OpenInterest_Agriculture'
_sqlTable_COMEX_Daily_Volume_OpenInterest_Energy        = 'COMEX_Daily_Volume_OpenInterest_Energy'
_sqlTable_COMEX_Daily_Volume_OpenInterest_Equity        = 'COMEX_Daily_Volume_OpenInterest_Equity'
_sqlTable_COMEX_Daily_Volume_OpenInterest_FX            = 'COMEX_Daily_Volume_OpenInterest_FX'
_sqlTable_COMEX_Daily_Volume_OpenInterest_InterestRate  = 'COMEX_Daily_Volume_OpenInterest_InterestRate'
_sqlTable_COMEX_Daily_Volume_OpenInterest_Metal         = 'COMEX_Daily_Volume_OpenInterest_Metal'

# ------ Fan's Laptop -------
# server = 'DESKTOP-45300G7'

def makeTodayDataDir(newDir):
    # if not myPath.lexists(newDir): #lexists
    if not myPath.exists(newDir):
        makedirs(newDir)

def getDateFromString_CME(dateStr):  
    b = dateStr.split("(")
    d = b[0].strip()        
    date_fromFile = d
    try:      
        date_fromFile = datetime.strptime(d, "%A, %B %d, %Y") #(d, "%Y/%m/%d") #(d, "%m/%d/%Y") 
    except ValueError:
        try:
            date_fromFile = datetime.strptime(d, "%A, %b %d, %Y")#(d, '%d %B %Y') # used LME
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
# a = 'Monday, May 10, 2021 ()'
# b = getDateFromString_CME(a)
# print (b)
 
"""
return the folder dir for the weekly SHFE data

""" 

def sql_daily_Vol_OI_comex(sourceFileFullpath, dbName):    
    df = pd.read_csv(sourceFileFullpath)    
    df = df.replace({np.NAN: None})
    df[df.columns[1]] = df[df.columns[1]].str.slice(0,60)
    print("sql insert file data: " + sourceFileFullpath)
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server+';DATABASE='+_database+';UID='+_username+';PWD='+_password)
    cursor = cnxn.cursor()
    
    for index, row in df.iterrows():
        query = """DELETE FROM %s where Date = '%s' and [Name] = '%s' and [Type] ='%s';""" \
                % (dbName, row[0], row[1], row[2])
        cursor.execute(query)         

        params = tuple(row)
        query = """INSERT INTO %s VALUES (?,?,?,?, ?,?,?,?, ?);""" %(dbName)
        cursor.execute(query, params)        
    cnxn.commit()        
    cursor.close()
    cnxn.close() 
# sourceFileFullpath = constCOMEX_A.CME_Vol_openInterest_Agricultural+ '/2021-05-03/2021-05-03_VoiTotalsByAssetClassExcelExport (4).csv'
# dbName = _sqlTable_COMEX_Daily_Vol_OpenInterest_Agriculture 
# sql_daily_Vol_OI_comex(sourceFileFullpath, dbName)  


def extract_CME_vol_OI_File(sourceFullpath): 
    print (sourceFullpath)
    df = pd.read_excel(sourceFullpath, dtype = object)
    df.replace(',','', regex=True, inplace=True)
    
    # df = pd.read_csv(sourceFullpath, names=col )
    df1 = df.dropna(how='all')
    df2 = df1.dropna(axis = 1, how='all')
    
    df3 = df2.iloc[2:-1]
    df3.columns = df2.iloc[0]
    filePath = constA.getFilePathInfo(sourceFullpath, 0) #/temp/2021-04-01
    date_fromFolderName  = constA.getFilePathInfo(filePath, 1) #2021-04-01     
    df3.insert(0, 'Date', date_fromFolderName)

    # cols = ['Globex','Open OutCry','Clear Port','Volume','Open Interest','Change']
    # df3[cols] = df3[cols].apply(pd.to_numeric, errors='coerce', axis=1)
    for col in  df3.columns[3:]:
        df3[col] = pd.to_numeric(df3[col], errors='coerce',downcast= 'integer')
    # dict1 = {'Globex': float ,'Open OutCry': float,'Clear Port': float,'Volume':float,'Open Interest': float,'Change': float}
    # df3 = df3.astype(dict1)
    
    #----get the date object and string
    filePath = constA.getFilePathInfo(sourceFullpath, 0)
    fileName = constA.getFilePathInfo(sourceFullpath, 2)  
    fileFullPath = filePath + '/' + date_fromFolderName + '_' +fileName + '.csv'

    df3.to_csv(fileFullPath, index = False) # float_format='%.3f')
    return fileFullPath
   
# sourceFullpath = constCOMEX_A.CME_Vol_openInterest_Agricultural+ '/2021-05-03/VoiTotalsByAssetClassExcelExport (4).xls'
# extract_CME_vol_OI_File(sourceFullpath)

def extrac_sql_subFolder(sourceDir, dbName):
    pathlist = Path(sourceDir).glob('**/*.xls')
    for path in pathlist: 
        sourceFullpath = str(path) 
        csvfileFullPath = extract_CME_vol_OI_File(sourceFullpath)        
        #---sql to db
        sourceFileFullpath = csvfileFullPath
        sql_daily_Vol_OI_comex(sourceFileFullpath, dbName)


# sourceDir = constCOMEX_A.CME_Vol_openInterest_Agricultural
# dbName = _sqlTable_COMEX_Daily_Vol_OpenInterest_Agriculture  
# extrac_sql_subFolder(sourceDir, dbName)

# sourceDir = constCOMEX_A.CME_Vol_openInterest_Energy 
# dbName = _sqlTable_COMEX_Daily_Volume_OpenInterest_Energy 
# extrac_sql_subFolder(sourceDir, dbName)

# sourceDir = constCOMEX_A.CME_Vol_openInterest_Equity
# dbName = _sqlTable_COMEX_Daily_Volume_OpenInterest_Equity  
# extrac_sql_subFolder(sourceDir, dbName)

# sourceDir = constCOMEX_A.CME_Vol_openInterest_FX
# dbName = _sqlTable_COMEX_Daily_Volume_OpenInterest_FX  
# extrac_sql_subFolder(sourceDir, dbName)

# sourceDir = constCOMEX_A.CME_Vol_openInterest_InterestRate
# dbName = _sqlTable_COMEX_Daily_Volume_OpenInterest_InterestRate
# extrac_sql_subFolder(sourceDir, dbName)

# sourceDir = constCOMEX_A.CME_Vol_openInterest_Metal
# dbName = _sqlTable_COMEX_Daily_Volume_OpenInterest_Metal  
# extrac_sql_subFolder(sourceDir, dbName)
    

def downloadExcelFile(targetDir, fileName, webAddress):
    makeTodayDataDir(targetDir)    
    newFilefullPath = targetDir + '/' + fileName + '.xls'   
    if os.path.isfile(newFilefullPath):
        os.remove(newFilefullPath)
        print('file removed: ' + newFilefullPath)
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3"}
    # reg_url = url
    req = Request(url = webAddress, headers = headers) 
    html = urlopen(req).read()  
    with open(newFilefullPath, 'wb') as outfile:
        outfile.write(html)   
    
    print('Downloaded COMEX daily Stock: ' + newFilefullPath)
    return newFilefullPath

def saveWebCME_daily_vol_OpenInterest(url, targetDir, fileName ):  
    driver = webdriver.Chrome('chromedriver.exe')  # Optional argument, if not specified will search path.
    dateDropDown_ID = 'tradesDropdown'
    dateDropDown_option_tagName = 'option'
    iconDownload_ID = 'excel'    

    driver.get(url)
    time.sleep(1)
    pyautogui.hotkey("f5")   
    time.sleep(1)      
    #-------get the date information
    date_field = driver.find_element_by_id(dateDropDown_ID)
    dateDropDown_Options = date_field.find_elements_by_tag_name(dateDropDown_option_tagName)
    dateDropDown_Options[0].click()
    dateStr1 = (dateDropDown_Options[0].text)
    dateStr = getDateFromString_CME(dateStr1)    
    # for option in date_field.find_elements_by_tag_name('option'):
    #     print(option.text)  Monday, May 10, 2021 
    
    href_field = driver.find_element_by_id(iconDownload_ID)   
    url_file = href_field.get_attribute('href')
    targetDir = targetDir + '/' + dateStr
    fileName2 = dateStr + '_'+ fileName   
    webAddress = url_file
    savedFileFullPath = downloadExcelFile(targetDir, fileName2, webAddress) 

    driver.quit()
    time.sleep(1)        
    return savedFileFullPath

def saveWebCME_daily_vol_OpenInterest_3(url, targetDir, fileName, driver ):  
    # driver = webdriver.Chrome('chromedriver.exe')  # Optional argument, if not specified will search path.
    dateDropDown_ID = 'tradesDropdown'
    dateDropDown_option_tagName = 'option'
    iconDownload_ID = 'excel'       

    driver.get(url)
    time.sleep(1)
    pyautogui.hotkey("f5")   
    time.sleep(1)     
    #-------get the date information
    date_field = driver.find_element_by_id(dateDropDown_ID)
    dateDropDown_Options = date_field.find_elements_by_tag_name(dateDropDown_option_tagName)
    #date_field.find_elements_by_tag_name('option'):
    time.sleep(1)    
    li = []
    for option in dateDropDown_Options:  
        dateStr1 = (option.text)
        dateStr = getDateFromString_CME(dateStr1)    
        option.click()
        time.sleep(1)    
        href_field = driver.find_element_by_id(iconDownload_ID)   
        url_file = href_field.get_attribute('href')
    # print (url_file)        
        targetDir2 = targetDir + '/' + dateStr
        fileName2 = dateStr + '_'+ fileName   
        webAddress = url_file
        savedFileFullPath = downloadExcelFile(targetDir2, fileName2, webAddress) 
        li.append(savedFileFullPath)
    # driver.quit()
    # time.sleep(1)        
    return li

def saveWebCME_daily_vol_OpenInterest_2(url, targetDir, fileName, driver ):  
    # driver = webdriver.Chrome('chromedriver.exe')  # Optional argument, if not specified will search path.
    dateDropDown_ID = 'tradesDropdown'
    dateDropDown_option_tagName = 'option'
    iconDownload_ID = 'excel'       

    driver.get(url)
    time.sleep(1)
    pyautogui.hotkey("f5")   
    time.sleep(3)     
    #-------get the date information
    date_field = driver.find_element_by_id(dateDropDown_ID)
    # for option in date_field.find_elements_by_tag_name('option'):
    dateDropDown_Options = date_field.find_elements_by_tag_name(dateDropDown_option_tagName)
    time.sleep(1)
    dateStr1 = (dateDropDown_Options[0].text)
    dateStr = getDateFromString_CME(dateStr1)      
    
    dateDropDown_Options[0].click()
    time.sleep(1)
    
    href_field = driver.find_element_by_id(iconDownload_ID)   
    url_file = href_field.get_attribute('href')
    # print (url_file)        
    targetDir2 = targetDir + '/' + dateStr
    fileName2 = dateStr + '_'+ fileName   
    webAddress = url_file
    savedFileFullPath = downloadExcelFile(targetDir2, fileName2, webAddress)
    # driver.quit()
    # time.sleep(1)        
    return savedFileFullPath

def CME_Vio_daily_run():
    driver = webdriver.Chrome('chromedriver.exe')  # Optional argument, if not specified will search path.
    #---------------------------        
    url			=constCOMEX_A.url_daily_Voi_Agricultural		
    targetDir	=constCOMEX_A.CME_Vol_openInterest_Agricultural 
    fileName	=constCOMEX_A.fileName_daily_Voi_Agricultural    
    fullPath_Agricultural = saveWebCME_daily_vol_OpenInterest_2(url, targetDir, fileName, driver )

       
    url			=constCOMEX_A.url_daily_Voi_Energy        
    targetDir	=constCOMEX_A.CME_Vol_openInterest_Energy 
    fileName	=constCOMEX_A.fileName_daily_Voi_Energy   
    fullPath_Energy = saveWebCME_daily_vol_OpenInterest_2(url, targetDir, fileName, driver )
    
    url			= constCOMEX_A.url_daily_Voi_Equity       
    targetDir	= constCOMEX_A.CME_Vol_openInterest_Equity
    fileName	= constCOMEX_A.fileName_daily_Voi_Equity  
    fullPath_Equity = saveWebCME_daily_vol_OpenInterest_2(url, targetDir, fileName, driver )

    url			= constCOMEX_A.url_daily_Voi_FX           
    targetDir	= constCOMEX_A.CME_Vol_openInterest_FX    
    fileName	= constCOMEX_A.fileName_daily_Voi_FX      
    fullPath_FX = saveWebCME_daily_vol_OpenInterest_2(url, targetDir, fileName, driver )
    
    url			=constCOMEX_A.url_daily_Voi_InterestRate		
    targetDir	=constCOMEX_A.CME_Vol_openInterest_InterestRate 
    fileName	=constCOMEX_A.fileName_daily_Voi_InterestRate	
    fullPath_InterestRate = saveWebCME_daily_vol_OpenInterest_2(url, targetDir, fileName, driver )

    url			=constCOMEX_A.url_daily_Voi_Metal		
    targetDir	=constCOMEX_A.CME_Vol_openInterest_Metal 
    fileName	=constCOMEX_A.fileName_daily_Voi_Metal   
    fullPath_Metal = saveWebCME_daily_vol_OpenInterest_2(url, targetDir, fileName, driver )
    
    #-----------------    
    driver.quit()
    time.sleep(1) 
    
    #----extrac files and save to SQL--------------------------------
    sourceFullpath = fullPath_Agricultural
    csvfileFullPath = extract_CME_vol_OI_File(sourceFullpath)        
    #---sql to db
    dbName = _sqlTable_COMEX_Daily_Vol_OpenInterest_Agriculture
    sql_daily_Vol_OI_comex(csvfileFullPath, dbName)    
    
    sourceFullpath = fullPath_Energy
    csvfileFullPath = extract_CME_vol_OI_File(sourceFullpath)        
    #---sql to db
    dbName = _sqlTable_COMEX_Daily_Volume_OpenInterest_Energy 
    sql_daily_Vol_OI_comex(csvfileFullPath, dbName)
    
    sourceFullpath = fullPath_Equity 
    csvfileFullPath = extract_CME_vol_OI_File(sourceFullpath)        
    #---sql to db
    dbName = _sqlTable_COMEX_Daily_Volume_OpenInterest_Equity 
    sql_daily_Vol_OI_comex(csvfileFullPath, dbName)
    
    sourceFullpath = fullPath_FX 
    csvfileFullPath = extract_CME_vol_OI_File(sourceFullpath)        
    #---sql to db
    dbName = _sqlTable_COMEX_Daily_Volume_OpenInterest_FX 
    sql_daily_Vol_OI_comex(csvfileFullPath, dbName)
    
    sourceFullpath = fullPath_InterestRate 
    csvfileFullPath = extract_CME_vol_OI_File(sourceFullpath)        
    #---sql to db
    dbName = _sqlTable_COMEX_Daily_Volume_OpenInterest_InterestRate 
    sql_daily_Vol_OI_comex(csvfileFullPath, dbName) 
    
    sourceFullpath = fullPath_Metal
    csvfileFullPath = extract_CME_vol_OI_File(sourceFullpath)        
    #---sql to db
    dbName = _sqlTable_COMEX_Daily_Volume_OpenInterest_Metal 
    sql_daily_Vol_OI_comex(csvfileFullPath, dbName)     
    
# CME_Vio_daily_run()    



