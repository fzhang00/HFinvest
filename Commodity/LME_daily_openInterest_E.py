# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 13:15:30 2021

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
# import ntpath
# from pathlib import Path
import pyodbc
import numpy as np
from urllib.request import urlopen, Request

#----------------------------------
errorFileTargetDir = '../'
pd.set_option('mode.chained_assignment', None)

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

_sqlTable_LME_daily_OpenInterest_option = 'LME_Daily_OpenInterest_Option_E'
_sqlTable_LME_daily_OpenInterest_future = 'LME_Daily_OpenInterest_Future_E'


_REPORT_DATE_col    = 'REPORT_DATE'
_FORWARD_DATE_col   = 'FORWARD_DATE'
_FORWARD_MONTH_col  = 'FORWARD_MONTH'


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
        d2 = d.strip()
        yy = datetime.strptime(d2, '%Y%m%d').strftime('%Y-%m-%d')
        df.iat[i, 0] = yy
    return df    

#----data extract part----------------------------------

def sql_openInterest_daily_Option(df, dbName): 
    # --- SQL ----
    df = df.replace({np.NAN: None})
    df[df.columns[2]] = df[df.columns[2]].str.slice(0,17)
    
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server+';DATABASE='+_database+';UID='+_username+';PWD='+_password)
    cursor = cnxn.cursor()
    
    #delete today data before enter
    dateStr = df.iloc[1,0]
    # productStr = row[1] 
    # descriptionStr  = row[2]       
    query = """DELETE FROM %s where Date = '%s';""" % (dbName, dateStr)
    cursor.execute(query)        
    
    for index, row in df.iterrows():     

        params = tuple(row)
        query = """INSERT INTO %s VALUES (?,?,?,?, ?,?,?,?);""" %(dbName)
        cursor.execute(query, params)        
    cnxn.commit()        
    cursor.close()
    cnxn.close()  
    
def sql_openInterest_daily_Future(df, dbName): 
    df = df.replace({np.NAN: None})
    df[df.columns[2]] = df[df.columns[2]].str.slice(0,17)

    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server+';DATABASE='+_database+';UID='+_username+';PWD='+_password)
    cursor = cnxn.cursor()    
    for index, row in df.iterrows(): 
        #delete today data before enter
        #Date	UNDERLYING	ContractType	ForwardDate	OpenInterest	Turnover
        
        
#--------disable this when load large files------------------------        
        query = """DELETE FROM %s where Date = '%s' and [Underlying] = '%s' and [ContractType] = '%s' and [ForwardDate] ='%s';""" \
                % (dbName, row[0], row[1], row[2],row[3])
        cursor.execute(query)          
#---------------------------------------

        
        params = tuple(row)
        query = """INSERT INTO %s VALUES (?,?,?,?, ?,? );""" %(dbName)
        cursor.execute(query, params)        
    cnxn.commit()        
    cursor.close()
    cnxn.close() 

def extract_OpenInterestData_Preciou_sql(fileFullPath, dbNameFuture):
    # df.astype(str)  # df = pd.read_csv(fileFullPath, dtype=str)   
    df = pd.read_csv(fileFullPath)    
    df1 = df.dropna(how='all')
    df_data = df1.dropna(axis = 1, how='all') 
    # df2 = df1.dropna(axis = 1, how='all') 
    
    #-- convert integer to datatime format
    df_data[_REPORT_DATE_col] = (pd.to_datetime(df_data[_REPORT_DATE_col], format = '%Y%m%d'))
    df_data[_FORWARD_DATE_col] = (pd.to_datetime(df_data[_FORWARD_DATE_col], format = '%Y%m%d')) 
   
    
    #--------aggrate the data   
    df_future = df_data.groupby([_REPORT_DATE_col,'UNDERLYING','CONTRACT_TYPE', 
                                 pd.Grouper(key=_FORWARD_DATE_col,freq='M') ]).agg({'OPEN_INTEREST':sum,'TURNOVER':sum})
    
    df_future1 = df_future.reset_index() 
    #----write the data to csv file.    
    if not df_future1.empty:        
        dateStr = df_future1.iloc[1,0].strftime('%Y-%m-%d')
        filePath = constA.getFilePathInfo(fileFullPath, 0)
        fileName = constA.getFilePathInfo(fileFullPath, 2)
        fileFullPath_new = filePath + '/' + dateStr + '_Future_' + fileName +'.csv'
        df_future1.to_csv(fileFullPath_new, index = False, date_format ='%Y-%m-%d')    
        print ("daily exchange options processed: " + fileFullPath)    
        
        #--------sql--------
        sql_openInterest_daily_Future(df_future1, dbNameFuture) 

# fileFullPath = constLME_a.commodityLME_openInterestDir_precious +'/Exchange Open Interest - precious - 05 May 2021.csv'
# dbNameFuture = _sqlTable_LME_daily_OpenInterest_future
# extract_OpenInterestData_Preciou_sql(fileFullPath, dbNameFuture)
# print()

    
def extract_OpenInterestData_Base_sql(fileFullPath, dbNameOption, dbNameFuture):
    # df.astype(str)  # df = pd.read_csv(fileFullPath, dtype=str)   
    df = pd.read_csv(fileFullPath)    
    df1 = df.dropna(how='all')
    # df_data = df1.dropna(axis = 1, how='all') 
    df2 = df1.dropna(axis = 1, how='all') 
    
    #------rows with AH and CA only
    boolseries = df2[df2.columns[1]].str.contains(r'ca|ah', case = False, na= False)   
    df_data = df2.loc[(boolseries)]
    # if df_data.empty:
    #     df_data = df2

    #-- convert integer to datatime format
    df_data[_REPORT_DATE_col] = (pd.to_datetime(df_data[_REPORT_DATE_col], format = '%Y%m%d'))
    df_data[_FORWARD_DATE_col] = pd.to_datetime(df_data[_FORWARD_DATE_col], format = '%Y%m%d')
    df_data[_FORWARD_MONTH_col] = pd.to_datetime(df_data[_FORWARD_MONTH_col], format = '%Y%m')

    #--------------
    #REPORT_DATE	UNDERLYING	CURRENCY	CONTRACT_TYPE	SUB_CONTRACT_TYPE	
    #FORWARD_DATE	FORWARD_MONTH	STRIKE	OPEN_INTEREST	TURNOVER
    #    pd.Grouper(key=('FORWARD_MONTH'), freq='MS',)  ] )['STRIKE'].mean() 
    #grouped['Points'].agg([np.sum, np.mean, np.std])
     # group.agg({'STRIKE' : 'mean' , 'OPEN_INTEREST': 'sum', 'TURNOVER': 'sum'})
     
     #--------aggrate the data
    df_option = df_data.groupby([_REPORT_DATE_col,'UNDERLYING', 'CONTRACT_TYPE',
                             'SUB_CONTRACT_TYPE', 
                             pd.Grouper(key=(_FORWARD_MONTH_col), freq='M',)  ] ).agg({'STRIKE' : 'mean' , 'OPEN_INTEREST': 'sum', 'TURNOVER': 'sum'})
    
    df_future = df_data.groupby([ _REPORT_DATE_col,'UNDERLYING', 'CONTRACT_TYPE', 
                             pd.Grouper(key=(_FORWARD_DATE_col), freq='M')  ] ).agg({'OPEN_INTEREST': 'sum', 'TURNOVER': 'sum'})

    df_option1 = df_option.reset_index()
    df_future1 = df_future.reset_index()  
    
    #----write the data to csv file.
    if not df_option1.empty:        
        dateStr = df_option1.iloc[1,0].strftime('%Y-%m-%d')
        filePath = constA.getFilePathInfo(fileFullPath, 0)
        fileName = constA.getFilePathInfo(fileFullPath, 2)
        fileFullPath_new = filePath + '/' + dateStr + '_Option_' + fileName +'.csv'
        df_option1.to_csv(fileFullPath_new, index = False, date_format ='%Y-%m-%d', float_format='%.1f' )    
        print ("daily exchange options processed: " + fileFullPath)

        #--------sql--------
        sql_openInterest_daily_Option(df_option1, dbNameOption)
    
    if not df_future1.empty:        
        dateStr = df_future1.iloc[1,0].strftime('%Y-%m-%d')
        filePath = constA.getFilePathInfo(fileFullPath, 0)
        fileName = constA.getFilePathInfo(fileFullPath, 2)
        fileFullPath_new = filePath + '/' + dateStr + '_Future_' + fileName +'.csv'
        df_future1.to_csv(fileFullPath_new, index = False, date_format ='%Y-%m-%d')    
        print ("daily exchange options processed: " + fileFullPath)    
        
        #--------sql--------
        sql_openInterest_daily_Future(df_future1, dbNameFuture)
    
    # #df['just_date'] = df['dates'].dt.date
    # for group_name, df_group in group:
    #     print (group_name) 
    #     print (df_group)
    #     print()    

# fileFullPath = constLME_a.commodityLME_openInterestDir_base +'/Exchange Open Interest - base - 06 May 2021.csv'
# dbNameOption = _sqlTable_LME_daily_OpenInterest_option
# dbNameFuture = _sqlTable_LME_daily_OpenInterest_future
# extract_OpenInterestData_Base_sql(fileFullPath, dbNameOption, dbNameFuture)
# print()



#-----------download part-------------------
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


def download_href_OpenInterest_daily(url, targetDir):
    driver = webdriver.Chrome('chromedriver.exe')
    driver.get(url)
    time.sleep(2) 

    elems = driver.find_elements_by_tag_name('a')
    time.sleep(1)
    count_First10File = 0
    list_fullPath = []    
    for elem in elems:
        href = elem.get_attribute('href')
        # time.sleep(1)
        # str_Inhref = 'StockBreakdownReportPaging'
        str_InText = 'exchange open interest'
        if str_InText in (elem.text).lower(): # if str_Inhref in href: # is not None: 
            count_First10File +=1
            # print(href)
            d1 = (elem.text).split('(')
            d2 = d1[0].split('.')
            fileName = d2[0].strip() + '.csv'
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


# url = 'https://www.lme.com/Market-Data/Reports-and-data/Open-interest/EOI#tabIndex=1'  
# url = constLME_a.dialyOpenInterest_base_url 
# targetDir = constLME_a.commodityLME_openInterestDir_base
# list_fullPath = download_href_OpenInterest_daily(url, targetDir)
# print (list_fullPath)

def LME_openInterest_daily():
    dbNameFuture = _sqlTable_LME_daily_OpenInterest_future         
    dbNameOption = _sqlTable_LME_daily_OpenInterest_option
    
    url = constLME_a.dialyOpenInterest_base_url 
    targetDir = constLME_a.commodityLME_openInterestDir_base
    list_fullPath = download_href_OpenInterest_daily(url, targetDir)      
    for i in range(len(list_fullPath)):
        print (list_fullPath) 
        fileFullPath = list_fullPath[i]
     
        extract_OpenInterestData_Base_sql(fileFullPath, dbNameOption, dbNameFuture)
    
    #-----precious metal---

    url = constLME_a.dialyOpenInterest_precious_url 
    targetDir = constLME_a.commodityLME_openInterestDir_precious
    list_fullPath = download_href_OpenInterest_daily(url, targetDir)
    for i in range(len(list_fullPath)):
        print (list_fullPath)     
        fileFullPath = list_fullPath[i]
        
        extract_OpenInterestData_Preciou_sql(fileFullPath, dbNameFuture)


# LME_openInterest_daily()





 
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

