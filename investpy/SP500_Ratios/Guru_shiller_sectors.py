# -*- coding: utf-8 -*-
"""
Created on Thu May 13 23:06:23 2021

@author: haoli
"""
# import sys
# sys.path.append("../")

import pandas as pd
from datetime import datetime
import pyodbc
import numpy as np

import win32com.client
import os
import ntpath
from urllib.request import urlopen, Request
import requests

# import SP500_Ratios.const_guru_shiller as myguruShiller
import investpy.SP500_Ratios.const_guru_shiller as myguruShiller
# import const_guru_shiller as myguruShiller

_server = 'RyanPC'
_database = 'SP500_Ratios' 
_username = 'hl' 
_password = '123'        

_sqlTable_SP500_Ratios_daily_sector_shillerPE = 'SP500_Ratios_daily_PE_sector_shillerPE'

pd.set_option('mode.chained_assignment', None)

#--------------------


def sql_guru_shillerRatio(df, dbName):
    df = df.replace({np.NAN: None})
    df[df.columns[1]] = df[df.columns[1]].str.slice(0,21) 
    
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server+';DATABASE='+_database+';UID='+_username+';PWD='+_password)
    cursor = cnxn.cursor()
    
    for index, row in df.iterrows():
        dateStr = row[0]     
        query = """DELETE FROM %s where Date = '%s' and [Sector] = '%s' and [ShillerPE] = %s and [RegulaPE] = %s ;""" % (dbName, dateStr, row[1], row[2], row[3])
        cursor.execute(query) 
        params = tuple(row)
        query = """INSERT INTO %s VALUES (?,?,?,? );""" %(dbName)
        cursor.execute(query, params)        
    cnxn.commit()        
    cursor.close()
    cnxn.close() 

    
def extrac_sql_guru_shillerRatio(csvFileFullPath, dbName):
    df1 = pd.read_csv(csvFileFullPath)
    df2 = df1.dropna(how='all')    
    df = df2.iloc[1:-1, :]
    df.columns = df1.columns
    
    df[df.columns[0]] = pd.to_datetime(df[df.columns[0]] , format='%Y-%m-%d')    
    for col in  df.columns[2:]:
        df[col] = pd.to_numeric(df[col], errors='coerce')#,downcast= 'integer')     
    # a = df.columns[0]
    df = df.replace({np.NAN: None})    
    df = df.sort_values(by = df.columns[0],  ascending=False)

    df.to_csv('guru_sp500Shiller_new.csv', index = False)
    
    for colName, coldata in df.iteritems():
        if 'unnamed' in colName.lower():
            pass
        else:
            sectorName = colName
            i = df.columns.get_loc(colName)
            # rows = 1 to last, col sector + 1
            df_data = df.iloc[ 1:-1 , [0, i, i+1]]
            df_data.insert(1, 'Sector', sectorName)            
            # print (i)
            # dbName = _sqlTable_SP500_Ratios_daily_sector_shillerPE
            sql_guru_shillerRatio(df, dbName)
            
# csvFileFullPath = myguruShiller.SP500_Ratios_dir_ShillerPE +'/GuruFocus_Sector_Shiller_PE_Historical_Data.xls.csv'
# sql_guru_shillerRatio(csvFileFullPath)
# print()

def extrac_sql_guru_shillerRatio2(csvFileFullPath, dbName, saveFileFullPath):
    df1 = pd.read_csv(csvFileFullPath)
    df2 = df1.dropna(how='all')    
    df = df2.iloc[1:-1, :]
    df.columns = df1.columns
    
    df[df.columns[0]] = pd.to_datetime(df[df.columns[0]] , format='%Y-%m-%d')    
    for col in  df.columns[2:]:
        df[col] = pd.to_numeric(df[col], errors='coerce')#,downcast= 'integer') 
    
    # a = df.columns[0]
    df = df.replace({np.NAN: None})    
    df = df.sort_values(by = df.columns[0],  ascending=False)

    df.to_csv(saveFileFullPath, index = False)
    
#-------sql---------------------    
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server+';DATABASE='+_database+';UID='+_username+';PWD='+_password)
    cursor = cnxn.cursor()  
    
#*****quick update*********************    
    df = df.head(5)
#******************************

    for colName, coldata in df.iteritems():
        if 'unnamed' in colName.lower():
            pass
        else:
            sectorName = colName
            i = df.columns.get_loc(colName)
            # rows = 1 to last, col sector + 1
            df_data = df.iloc[ : , [0, i, i+1]]
            df_data.insert(1, 'Sector', sectorName)
            df_data[df_data.columns[1]] = df_data[df_data.columns[1]].str.slice(0,21)           
            print(sectorName)
            
            for index, row in df_data.iterrows():
                #----comment out for fast operation-----
                dateStr = row[0]     
                query = """DELETE FROM %s where Date = '%s' and [Sector] = '%s' and [ShillerPE] = %s and [RegulaPE] = %s ;""" % (dbName, dateStr, row[1], row[2], row[3])
                cursor.execute(query) 
                
                params = tuple(row)
                query = """INSERT INTO %s VALUES (?,?,?,? );""" %(dbName)
                cursor.execute(query, params) 
                
    cnxn.commit()        
    cursor.close()
    cnxn.close() 
            
# csvFileFullPath = myguruShiller.SP500_Ratios_dir_ShillerPE +'/GuruFocus_Sector_Shiller_PE_Historical_Data.xls.csv'
# dbName = _sqlTable_SP500_Ratios_daily_sector_shillerPE
# saveFileFullPath = myguruShiller.SP500_Ratios_dir_PE + '/guru_sp500_PE_SectorShiller_dailyUpdated.csv'
# extrac_sql_guru_shillerRatio2(csvFileFullPath, dbName, saveFileFullPath)

def excel_to_CSV_guru(fileFullPath):     
    fileAbsPath = os.path.abspath(fileFullPath)   
    winPath = fileAbsPath.replace(os.sep,ntpath.sep)   
    xlApp = win32com.client.Dispatch('Excel.Application')
    xlApp.Visible = False
    xls = xlApp.Workbooks.Open(winPath)

    csvFileFullPath = winPath+".csv"
    if os.path.isfile( csvFileFullPath):
        os.remove( csvFileFullPath)
        print('file removed: ' + fileFullPath)    
    xls.SaveAs( csvFileFullPath, FileFormat=6)
    # xls.close()
    xlApp.quit()
    return csvFileFullPath
# fileFullPath = myguruShiller.SP500_Ratios_dir_ShillerPE +'/GuruFocus_Sector_Shiller_PE_Historical_Data.xls'
# csvFileFullPath = excel_to_CSV_guru(fileFullPath)    
# print(csvFileFullPath)  

#-------donwload files-------------------------------
def downloadExcelFile(targetDir, fileName, webAddress):
    # makeTodayDataDir(targetDir)    
    newFilefullPath = targetDir + '/' + fileName
    
    if os.path.isfile(newFilefullPath):
        os.remove(newFilefullPath)
        print('file removed: ' + newFilefullPath)
    
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3"}
    # reg_url = url
    req = Request(url = webAddress, headers = headers) 
    html = urlopen(req).read()  
    with open(newFilefullPath, 'wb') as outfile:
        outfile.write(html)   
    
    print('Downloaded Guru sp500 shillerPE daily: ' + newFilefullPath)
    return newFilefullPath


def guru_sp500_PE_shillerSector_daily():    
    targetDir = myguruShiller.SP500_Ratios_dir_ShillerPE 
    fileName = datetime.today().strftime('%Y-%m-%d') +'_' + 'GuruFocus_Sector_Shiller_PE_Historical_Data.xls'
    webAddress = myguruShiller._Guru_shillerSector_URL
    
    newExcel_FilefullPath = downloadExcelFile(targetDir, fileName, webAddress)
    csvFileFullPath = excel_to_CSV_guru(newExcel_FilefullPath)
    
    # csvFileFullPath = myguruShiller.SP500_Ratios_dir_ShillerPE +'/GuruFocus_Sector_Shiller_PE_Historical_Data.xls.csv'
    dbName = _sqlTable_SP500_Ratios_daily_sector_shillerPE
    saveFileFullPath = myguruShiller.SP500_Ratios_dir_PE + '/guru_sp500_PE_SectorShiller_dailyUpdated.csv'
    extrac_sql_guru_shillerRatio2(csvFileFullPath, dbName, saveFileFullPath)
 
# guru_sp500_PE_shillerSector_daily()
    
#------------------------------------------

# url = myguruShiller._multpl_shillerTotal_URL
# saveFileFullPath = myguruShiller.SP500_Ratios_dir_PE + '/Multpl_sp500_shiller_dailyUpdated.csv'
# dbName = _sqlTable_SP500_Ratios_daily_sector_shillerPE

def multpl_sp500Total_shillerPE_daily(url, saveFileFullPath, dbName):
    list0 = pd.read_html(url) 
    df1 = list0[0]
        #	Date	May 14, 2021
    df = pd.DataFrame()
    df['Date'] = pd.to_datetime(df1[df1.columns[0]] , format='%b %d, %Y')
    df['Sector'] = 'SP500'
    df['Shiller'] = pd.to_numeric(df1[df1.columns[1]], errors='coerce') 
    df['Regular'] = None
   
    df = df.replace({np.NAN: None})    
    df = df.sort_values(by = df.columns[0],  ascending=False)
    df4 = df.head(1)
    df4.to_csv(saveFileFullPath, mode='a', index = False, header=False)

    
#-------sql---------------------    
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server+';DATABASE='+_database+';UID='+_username+';PWD='+_password)
    cursor = cnxn.cursor()  
    
#*****quick update*********************    
    df = df.head(1)
#******************************

    for index, row in df.iterrows():
        if row[0] < pd.to_datetime('1900-01-01', format='%Y-%m-%d'):
            break
        dateStr = row[0]     
        query = """DELETE FROM %s where Date = '%s' and [Sector] = '%s' and [ShillerPE] = %s and ([RegulaPE] IS NULL) ;""" % (dbName, dateStr, row[1], row[2])
        cursor.execute(query) 
        print (row[0])
        params = tuple(row)
        query = """INSERT INTO %s VALUES (?,?,?,? );""" %(dbName)
        cursor.execute(query, params) 
                
    cnxn.commit()        
    cursor.close()
    cnxn.close() 
# url = myguruShiller._multpl_shillerTotal_URL
# saveFileFullPath = myguruShiller.SP500_Ratios_dir_PE + '/Multpl_sp500_shiller_dailyUpdated.csv'
# dbName = _sqlTable_SP500_Ratios_daily_sector_shillerPE

# multpl_sp500Total_shillerPE_daily(url, saveFileFullPath, dbName)



def guru_sp500_PE_TotalNormal_daily(url, dbName, saveFileFullPath):
    # url = 'https://www.investing.com/earnings-calendar/'    
    header = {
      "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
      "X-Requested-With": "XMLHttpRequest"
    }    
    r = requests.get(url, headers=header)    
    dfs = pd.read_html(r.text)
    
    df1 = dfs[1]

    df = pd.DataFrame()
    df['Date'] = pd.to_datetime(df1[df1.columns[0]] , format='%Y-%m-%d')
    df['Sector'] = 'SP500'
    df['Shiller'] = None 
    df['Regular'] = pd.to_numeric(df1[df1.columns[1]], errors='coerce')   
    df = df.replace({np.NAN: None})    
    df = df.sort_values(by = df.columns[0],  ascending=False)
#********    
    # df4 = df.head(5)
    df4 = df
#********       
    df4.to_csv(saveFileFullPath, mode='a', index = False, header=False)
    df_a = pd.read_csv(saveFileFullPath).drop_duplicates()
    df_b = df_a.sort_values(by = [df_a.columns[0]])    
    df_b.to_csv(saveFileFullPath, index = False, float_format = '%.3f')
    
#-------sql---------------------    
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server+';DATABASE='+_database+';UID='+_username+';PWD='+_password)
    cursor = cnxn.cursor() 
#*****quick update*********************    
    df = df.head(15)
#******************************
    for index, row in df.iterrows():
        # if row[0] < pd.to_datetime('1900-01-01', format='%Y-%m-%d'):
        #     break
        dateStr = row[0]     
        query = """DELETE FROM %s where Date = '%s' and [Sector] = '%s' and [ShillerPE] IS NULL and ([RegulaPE] = '%s') ;""" % (dbName, dateStr, row[1], row[3])
        cursor.execute(query) 
        # print (row[0])
        params = tuple(row)
        query = """INSERT INTO %s VALUES (?,?,?,? );""" %(dbName)
        cursor.execute(query, params)                 
    cnxn.commit()        
    cursor.close()
    cnxn.close() 

# url = myguruShiller._Guru_sp500_PE_totalNormal_URL
# dbName = _sqlTable_SP500_Ratios_daily_sector_shillerPE
# saveFileFullPath = myguruShiller.SP500_Ratios_dir_PE + '/Guru_sp500_PE_TotalNormal_dailyUpdated.csv'
# guru_sp500_PE_TotalNormal_daily(url, dbName, saveFileFullPath)
# print()


def Multpl_sp500_PE_TotalNormal_monthly(fileFullPath, dbName):
    df1 = pd.read_csv(fileFullPath)

    df = pd.DataFrame()
    df['Date'] = pd.to_datetime(df1[df1.columns[0]] , format='%Y-%m-%d')
    df['Sector'] = 'SP500'
    df['Shiller'] = None 
    df['Regular'] = pd.to_numeric(df1[df1.columns[1]], errors='coerce')   
    df = df.replace({np.NAN: None})    
    df = df.sort_values(by = df.columns[0],  ascending=False)
    
#-------sql---------------------    
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server+';DATABASE='+_database+';UID='+_username+';PWD='+_password)
    cursor = cnxn.cursor() 
    for index, row in df.iterrows():
        if row[0] < pd.to_datetime('1900-01-01', format='%Y-%m-%d'):
            break
        # dateStr = row[0]     
        # query = """DELETE FROM %s where Date = '%s' and [Sector] = '%s' and [ShillerPE] IS NULL and ([RegulaPE] = '%s') ;""" % (dbName, dateStr, row[1], row[3])
        # cursor.execute(query) 
        # print (row[0])
        params = tuple(row)
        query = """INSERT INTO %s VALUES (?,?,?,? );""" %(dbName)
        cursor.execute(query, params)                 
    cnxn.commit()        
    cursor.close()
    cnxn.close() 

# fileFullPath = myguruShiller.SP500_Ratios_dir_PE + '/backup/MULTPL-SP500_PE_RATIO_MONTH.csv'
# dbName = _sqlTable_SP500_Ratios_daily_sector_shillerPE
# Multpl_sp500_PE_TotalNormal_monthly(fileFullPath, dbName)
# print()


def sp500_daily_run_PE():
    dbName = _sqlTable_SP500_Ratios_daily_sector_shillerPE
    
    #----mulpl shiller total PE------
    url = myguruShiller._multpl_shillerTotal_URL
    saveFileFullPath = myguruShiller.SP500_Ratios_dir_PE + '/Multpl_sp500_PE_TotalShiller_dailyUpdated.csv'
    multpl_sp500Total_shillerPE_daily(url, saveFileFullPath, dbName) 
    
    #---------guru total normal PE-------------
    url = myguruShiller._Guru_sp500_PE_totalNormal_URL
    saveFileFullPath = myguruShiller.SP500_Ratios_dir_PE + '/Guru_sp500_PE_TotalNormal_dailyUpdated.csv'
    guru_sp500_PE_TotalNormal_daily(url, dbName, saveFileFullPath)
    
    #-----------Sector-----------------
    guru_sp500_PE_shillerSector_daily()
    
# sp500_daily_run_PE()


    
#___________-----------


# import xlrd
# def sql_excelFile_SP500_Ratios_dir_ShillerPE(fileFullPath, dbName):
 
#     col = ['Date',	'Basic Materials',	'c1',	'Consumer Cyclical',	'c2',	
#            'Financial Services',	'c3',	'Real Estate',	'c4',	'Consumer Defensive',	'c5',
#            'Healthcare',	'c6',	'Utilities',	'c7',	'Communication Services',	'c8',	
#            'Energy',	'c9',	'Industrials',	'c10',	'Technology',	'c11' ]
    
#     # df = pd.read_excel(fileFullPath, engine='custom_xlrd',  names = col) 



#     workbook = xlrd.open_workbook(fileFullPath, ignore_workbook_corruption =True )
#     excel = pd.read_excel(workbook, names = col)

    
#     df[colDate] = pd.to_datetime(df[colDate], format = '%Y-%m') 
#     for col in  df.columns[1:]:
#         df[col] = pd.to_numeric(df[col], errors='coerce',downcast= 'integer')        
#     sql_monthly_marginStast(df, dbName)
    
# # fileFullPath =  myguruShiller.SP500_Ratios_dir_ShillerPE + '/GuruFocus_Sector_Shiller_PE_Historical_Data.xls'
# fileFullPath =  myguruShiller.SP500_Ratios_dir_ShillerPE + '/GuruFocus_Sector_Shiller_PE_Historical_Data.csv'
# dbName = _sqlTable_Sector_Shiller_PE_   
# # sql_excelFile_SP500_Ratios_dir_ShillerPE(fileFullPath, dbName) 

# class CustomXlrdReader(_XlrdReader):
#     def load_workbook(self, filepath_or_buffer):
#         """Same as original, just uses ignore_workbook_corruption=True)"""
#         from xlrd import open_workbook

#         if hasattr(filepath_or_buffer, "read"):
#             data = filepath_or_buffer.read()
#             return open_workbook(file_contents=data, ignore_workbook_corruption=True)
#         else:
#             return open_workbook(filepath_or_buffer)
 
        
# 



