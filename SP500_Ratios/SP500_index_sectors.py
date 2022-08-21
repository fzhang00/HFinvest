# -*- coding: utf-8 -*-
"""
Created on Thu May 13 23:06:23 2021

@author: haoli
"""
import sys
sys.path.append("../")

import pandas as pd
from datetime import datetime
import pyodbc
import numpy as np

import win32com.client
import os
import ntpath
from urllib.request import urlopen, Request
import requests
from selenium import webdriver
import time

import pandas_datareader as web
import datetime as dt


import key as pconst
_server = pconst.RYAN_SQL['server']
_username = pconst.RYAN_SQL['username']
_password = pconst.RYAN_SQL['password']  
_database = 'SP500_Ratios'     

#-----------------------------------------------
# _dir_sp500_ratio = './ratio/'
_dir_sp500_value = './value/'
_dir_sp500_SectorWeight = './SectorWeight/'
'https://en.wikipedia.org/wiki/Global_Industry_Classification_Standard'
#----------------
# _sqlTable_SP500_Ratios_daily_sector_shillerPE = 'SP500_Ratios_daily_PE_sector_shillerPE'
_sqlTable_SP500_ClosePrice = 'SP500_ClosePrice' 
# _sqlTable_SP500_ClosePrice_Sector = 'SP500_ClosePrice_Sector'
# _sqlTable_SP500_Volume_Sector = 'SP500_Volume_Sector'

_sqlTable_SP500_Sector_Weight = 'SP500_Sector_Weight'
_sqlTable_SP500_Sector_PriceVolume = 'SP500_Sector_PriceVolume'
_sqlTable_SP500_Sector_Industry_MarketCap = 'SP500_Sector_Industry_MarketCap'



pd.set_option('mode.chained_assignment', None)

# df = pd.read_html('https://en.wikipedia.org/wiki/Global_Industry_Classification_Standard')

# df = pd.read_html('https://eresearch.fidelity.com/eresearch/markets_sectors/sectors/sectors_in_market.jhtml')

#--------------------


def sql_Date_Value(dbName, df):
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server+';DATABASE='+_database+';UID='+_username+';PWD='+_password)
    cursor = cnxn.cursor()      
    for index, row in df.iterrows():
        dateStr = row[0]     
        query = """DELETE FROM %s where Date = '%s';""" % (dbName, dateStr)
        cursor.execute(query)         
        params = tuple(row)
        query = """INSERT INTO %s VALUES (?,?);""" %(dbName)
        cursor.execute(query, params) 
        cnxn.commit()
        # break            
    cursor.close()
    cnxn.close() 
    

def sp500_closePrice():  
    today = datetime.today()
    todayOffset2 = today - dt.timedelta(14)
    # raw_data = web.DataReader('^GSPC', 'yahoo', datetime.datetime(2022, 2, 5), datetime.datetime(2022, 2, 6), api_key=None)
    raw_data = web.DataReader('^GSPC', 'yahoo', todayOffset2, today, api_key=None)
    raw_data.reset_index(inplace=True)
    dbName = _sqlTable_SP500_ClosePrice
    # df=pd.read_excel("./ratio/IndexPrice.xlsx") 
    df = pd.DataFrame()
    df = raw_data[['Date','Close']]
    df['Close'] = df['Close'].round(2)
    sql_Date_Value(dbName, df)
    print("SP500 close price downlaoded, sql")

# def sp500_closePrice_volume():  
#     today = datetime.today()
#     # todayOffset2 = today - dt.timedelta(5)
#     todayOffset2 = datetime(1970, 1, 5)
#     # raw_data = web.DataReader('^GSPC', 'yahoo', datetime.datetime(2022, 2, 5), datetime.datetime(2022, 2, 6), api_key=None)
#     raw_data = web.DataReader('^GSPC', 'yahoo', todayOffset2, today, api_key=None)
#     raw_data.reset_index(inplace=True)
#     raw_data = raw_data.round(2)    
#     saveFileFullPath = _dir_sp500_value + 'SP500_History.csv'
#     raw_data.to_csv(saveFileFullPath, index = False)    
# sp500_closePrice_volume()

def sector_Price_Volume():
    today = datetime.today()
    todayOffset2 = today - dt.timedelta(7)
    # todayOffset2 = datetime(1993, 5, 3)
    
    s5TELS = web.DataReader('^SP500-50', 'yahoo', todayOffset2, today, api_key=None)
    s5COND = web.DataReader('^SP500-25', 'yahoo', todayOffset2, today, api_key=None)
    s5CONS = web.DataReader('^SP500-30', 'yahoo', todayOffset2, today, api_key=None)

    sPN     = web.DataReader('^GSPE', 'yahoo', todayOffset2, today, api_key=None)    
    sPF     = web.DataReader('^SP500-40', 'yahoo', todayOffset2, today, api_key=None)
    s5HLTH = web.DataReader('^SP500-35', 'yahoo', todayOffset2, today, api_key=None)
    
    s5INDU = web.DataReader('^SP500-20', 'yahoo', todayOffset2, today, api_key=None)
    s5INFT = web.DataReader('^SP500-45', 'yahoo', todayOffset2, today, api_key=None)
    s5MATR = web.DataReader('^SP500-15', 'yahoo', todayOffset2, today, api_key=None)
    
    s5UTIL = web.DataReader('^SP500-55', 'yahoo', todayOffset2, today, api_key=None)    
    s5REAS = web.DataReader('^SP500-60', 'yahoo', todayOffset2, today, api_key=None)

    s5TELS['Sector'] = 's5TELS'
    s5COND['Sector'] = 's5COND'
    s5CONS['Sector'] = 's5CONS'
    sPN['Sector']  ='sPN'
    sPF['Sector']  ='sPF'
    s5HLTH['Sector'] = 's5HLTH'
    s5INDU['Sector'] = 's5INDU'
    s5INFT['Sector'] = 's5INFT'
    s5MATR['Sector'] = 's5MATR'
    s5UTIL['Sector'] = 's5UTIL'   
    s5REAS['Sector'] = 's5REAS'
       
    dfx =[s5TELS[['Sector','Close','Volume']],    s5COND[['Sector','Close','Volume']],  s5CONS[['Sector','Close','Volume']], 
          sPN[['Sector','Close','Volume']],       sPF[['Sector','Close','Volume']],     s5HLTH[['Sector','Close','Volume']],
          s5INDU[['Sector','Close','Volume']],    s5INFT[['Sector','Close','Volume']],  s5MATR[['Sector','Close','Volume']],
          s5UTIL[['Sector','Close','Volume']],    s5REAS[['Sector','Close','Volume']]           ] 
    df = pd.concat(dfx)  #df = pd.concat(dfx, axis=1)
    df.reset_index(inplace=True)

    df = df.round(2).replace({np.NAN: None}) 
    df =df.sort_values(by= df.columns[0], ascending = True)    
    # saveFileFullPath = _dir_sp500_value + 'sector_Price_Volume.csv'
    # # df.to_csv(saveFileFullPath, mode='a', index = False, header=False)
    # df.to_csv(saveFileFullPath, index = False)
    
    dbName = _sqlTable_SP500_Sector_PriceVolume
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server+';DATABASE='+_database+';UID='+_username+';PWD='+_password)
    cursor = cnxn.cursor()      
    for index, row in df.iterrows():
        dateStr = row[0]     
        query = """DELETE FROM %s where Date = '%s' and [Sector] = '%s';""" % (dbName, dateStr, row[1])
        cursor.execute(query)         
        params = tuple(row)
        query = """INSERT INTO %s VALUES (?,?,?,?);""" %(dbName)
        cursor.execute(query, params) 
        cnxn.commit()
        # break            
    cursor.close()
    cnxn.close()     
    print("SP500 11 sectors - close price and volume downlaoded, sql") 
# sector_Price_Volume()
# print()  


#--------fidelity ------------------------------
def webpage_SP500_marketWeight_Sector():   
    url = 'https://eresearch.fidelity.com/eresearch/markets_sectors/sectors/si_weighting_recommendations.jhtml?tab=sirecommendations'       
    driver = webdriver.Chrome('../chromedriver.exe')
    driver.implicitly_wait(10)    
    driver.get(url)
    time.sleep(2)
    tables = pd.read_html(driver.page_source)
    df = tables[0]

    d1 = (df.columns.values.tolist())[1][1]
    d= (d1.lower()).split(('market weight'))[1]
    
    dateStr = ''
    try: # DD-MM-YYYY        
        dateStr = (pd.to_datetime(d.strip() , format='%m/%d/%Y')).strftime('%Y-%m-%d')
    except ValueError:
        print ("-- Error: date convert error.  sp500 sector market weight ")
        
    df.insert(0, 'Date', dateStr)
    df[df.columns[2]] = df[df.columns[2]].str.replace('%', '')
    
    saveFileFullPath = _dir_sp500_SectorWeight + datetime.today().strftime('%Y') + '-MarketWeight.csv'
    df.to_csv(saveFileFullPath, mode='a', index = False, header=False)
    
    driver.quit()
    #---------database------------------
    dbName = _sqlTable_SP500_Sector_Weight
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server+';DATABASE='+_database+';UID='+_username+';PWD='+_password)
    cursor = cnxn.cursor()      
    for index, row in df.iterrows():
        dateStr = row[0]     
        query = """DELETE FROM %s where [Date] = '%s' and [Sector] = '%s' ;""" % (dbName, dateStr, row[1])
        cursor.execute(query)         
        params = tuple([row[0],row[1],row[2]])
        query = """INSERT INTO %s VALUES (?,?,?);""" %(dbName)
        cursor.execute(query, params) 
        cnxn.commit()
        # break            
    cursor.close()
    cnxn.close()    
    print("SP500 sector weight downlaoded, sql")    
# webpage_SP500_marketWeight_Sector()
# print()

def webpage_SP500_marketCap_Industry():   
    url = 'https://eresearch.fidelity.com/eresearch/markets_sectors/sectors/sectors_in_market.jhtml'       
    driver = webdriver.Chrome('../chromedriver.exe')
    driver.implicitly_wait(10)    
    driver.get(url)
    time.sleep(2)
    
    # driver.find_element_by_class_name("collapse-all").click()
    # time.sleep(3)
    tables_sector = pd.read_html(driver.page_source)
    if len(tables_sector) == 2 and len(tables_sector[0] == 12):
        pass
    else:
        driver.get(url)
        time.sleep(2)
        tables_sector = pd.read_html(driver.page_source)
        if len(tables_sector) == 2 and len(tables_sector[0] == 12):
            pass
        else:            
            print ("Error:  check the websize of SP500 market Cap -  sectors and industry")
            return
    #-----------get date from the header
    df = tables_sector[0]
    d1 = (df.columns.values.tolist())[1]
    dd= (d1.lower()).split(('et'))[1]
    
    dateStr = ''
    try: # DD-MM-YYYY        
        dateStr = (pd.to_datetime(dd.strip() , format='%m/%d/%Y')).strftime('%Y-%m-%d')
    except ValueError:
        print ("-- Error: date convert error.  sp500 sector and industry market cap ")         
        
    #---get the sector name and market cap
    df1 = tables_sector[0]
    df2 = (df1[df1.columns[0]]).str.split('details', expand=True)
    df1[df1.columns[0]] = df2[df2.columns[1]].str.lower().str.replace('industries',"").str.strip()
    
    df_sector = df1[ [df1.columns[0], df1.columns[2] ]]
    
    driver.find_element_by_class_name("expand-all").click()
    time.sleep(2)
    tables_industry = pd.read_html(driver.page_source)
    
    df = pd.DataFrame()
    # df_industry = pd.DataFrame()
    for i in range(len(df_sector) ):
        dfx = tables_industry[i+1]
        df_industry = dfx[ [dfx.columns[0], dfx.columns[2] ]]
        pass
        # dfx1 = df_industry.append([df_sector.iat[i, 0] ,  df_sector.iat[i, 1])] , ignore_index = True)
        df_industry.loc[-1] = df_sector.loc[i].values.tolist() #df_sector.loc[i]
        # df_industry.reset_index(inplace=True)
        
        df_industry.insert(0, "Sector", df_sector.iloc[i,0])# add the sector name col        
        df = pd.concat([ df,df_industry ])
        i +=1
        if i == 11:
            break
    df.insert(0, 'Date', dateStr)
    # df.reset_index(inplace=True) '$': '', 
    df.reset_index(drop = True, inplace=True)

    df[df.columns[3]] = (df[df.columns[3]]).str.replace('[$,B]', '')
    df[df.columns[3]] = (df[df.columns[3]]).str.replace('T', '*1e3')
    df[df.columns[3]] = pd.eval(df[df.columns[3]])    
    
    saveFileFullPath = _dir_sp500_SectorWeight + datetime.today().strftime('%Y') + '-Industry MarketCapital.csv'
    df.to_csv(saveFileFullPath, mode='a', index = False, header=False)    

    driver.quit()
    
    #---------database------------------
    saveFileFullPath_temp = _dir_sp500_SectorWeight + 'temp Industry MarketCapital.csv'
    df.to_csv(saveFileFullPath_temp, index= False)
    df = pd.read_csv(saveFileFullPath_temp)
    
    dbName = _sqlTable_SP500_Sector_Industry_MarketCap
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server+';DATABASE='+_database+';UID='+_username+';PWD='+_password)
    cursor = cnxn.cursor()      
    for index, row in df.iterrows():
        # dateStr = row[0]     
        query = """DELETE FROM %s where [Date] = '%s' and [Sector] = '%s' and [Industry] = '%s' ;""" % (dbName, row[0] , row[1], row[2])
        # query = """DELETE FROM %s where [Date] = '%s' and [Sector] = '%s' ;""" % (dbName, row[0] , row[1])        
        cursor.execute(query)         
        # params = tuple([row[0],row[1],row[2],row[3]])
        params = tuple(row)
        query = """INSERT INTO %s VALUES (?,?,?,?);""" %(dbName)
        cursor.execute(query, params) 
        cnxn.commit()
        # break            
    cursor.close()
    cnxn.close()    
    print("SP500 sector-Industry market cap downlaoded, sql")  
    
# webpage_SP500_marketCap_Industry()
# print()       
#-------------------------------------------

#------------------------------------------------ 

#------------------------------------------
def sp500_daily_run_PE():  
    if datetime.today().weekday() == 6:
        return
        #-----------Sector-----------------
    elif datetime.today().weekday() == 5:
        pass
    else:     
        sp500_closePrice()
        sector_Price_Volume()
        webpage_SP500_marketWeight_Sector()
        webpage_SP500_marketCap_Industry()
    
sp500_daily_run_PE()
# sp500_closePrice()
# sector_Price_Volume()
# webpage_SP500_marketWeight_Sector()
# webpage_SP500_marketCap_Industry()
        
# webpage_SP500_marketWeight_Sector()



# def sector_Price_Vol_outterJoin():
#     today = datetime.today()
#     todayOffset2 = today - dt.timedelta(14)
#     # todayOffset2 = datetime(1993, 5, 3)
    
#     # raw_data = web.DataReader('^GSPC', 'yahoo', datetime.datetime(2022, 2, 5), datetime.datetime(2022, 2, 6), api_key=None)
#     s5TELS = web.DataReader('^SP500-50', 'yahoo', todayOffset2, today, api_key=None)
#     s5COND = web.DataReader('^SP500-25', 'yahoo', todayOffset2, today, api_key=None)
#     s5CONS = web.DataReader('^SP500-30', 'yahoo', todayOffset2, today, api_key=None)

#     sPN     = web.DataReader('^GSPE', 'yahoo', todayOffset2, today, api_key=None)    
#     sPF     = web.DataReader('^SP500-40', 'yahoo', todayOffset2, today, api_key=None)
#     s5HLTH = web.DataReader('^SP500-35', 'yahoo', todayOffset2, today, api_key=None)
    
#     s5INDU = web.DataReader('^SP500-20', 'yahoo', todayOffset2, today, api_key=None)
#     s5INFT = web.DataReader('^SP500-45', 'yahoo', todayOffset2, today, api_key=None)
#     s5MATR = web.DataReader('^SP500-15', 'yahoo', todayOffset2, today, api_key=None)
    
#     s5UTIL = web.DataReader('^SP500-55', 'yahoo', todayOffset2, today, api_key=None)    
#     s5REAS = web.DataReader('^SP500-60', 'yahoo', todayOffset2, today, api_key=None)

#     dfx =[s5TELS['Close'],    s5COND['Close'],  s5CONS['Close'], 
#           sPN['Close'],       sPF['Close'],     s5HLTH['Close'],
#           s5INDU['Close'],    s5INFT['Close'],  s5MATR['Close'],
#           s5UTIL['Close'],    s5REAS['Close']           ] 
#     df = pd.concat(dfx, axis=1)
#     df.reset_index(inplace=True)
#     df = df.round(2).replace({np.NAN: None}) 

#     # saveFileFullPath = _dir_sp500_value + 'sector_closePrice.csv'
#     # df.to_csv(saveFileFullPath, mode='a', index = False, header=False)
#     # df.to_csv(saveFileFullPath, index = False)
#     dbName = _sqlTable_SP500_ClosePrice_Sector
#     sql_Date_Value_12col(dbName, df)
    
    
#     dfx =[s5TELS['Volume'],    s5COND['Volume'],  s5CONS['Volume'], 
#           sPN['Volume'],       sPF['Volume'],     s5HLTH['Volume'],
#           s5INDU['Volume'],    s5INFT['Volume'],  s5MATR['Volume'],
#           s5UTIL['Volume'],    s5REAS['Volume']           ] 
#     df = pd.concat(dfx, axis=1)
#     df.reset_index(inplace=True)    
#     df = df.replace({np.NAN: None})      
#     # saveFileFullPath = _dir_sp500_value + 'sector_closePrice.csv'
#     # df.to_csv(saveFileFullPath, mode='a', index = False, header=False)
#     # df.to_csv(saveFileFullPath, index = False)
#     dbName = _sqlTable_SP500_Volume_Sector
#     sql_Date_Value_12col(dbName, df)    
#     print("SP500 11 sectors - close price and volume downlaoded, sql") 
# # sector_Price_Vol_outterJoin()
# # print()  


# def sql_Date_Value_12col(dbName, df):
#     cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server+';DATABASE='+_database+';UID='+_username+';PWD='+_password)
#     cursor = cnxn.cursor()      
#     for index, row in df.iterrows():
#         dateStr = row[0]     
#         query = """DELETE FROM %s where Date = '%s';""" % (dbName, dateStr)
#         cursor.execute(query)         
#         params = tuple(row)
#         query = """INSERT INTO %s VALUES (?,?,?,?);""" %(dbName)
#         cursor.execute(query, params) 
#         cnxn.commit()
#         # break            
#     cursor.close()
#     cnxn.close()  
# dbName = _sqlTable_SP500_Volume_Sector
# saveFileFullPath = _dir_sp500_value + 'sector_volume 1993-2022.csv'
# df = pd.read_csv(saveFileFullPath)
# df = df.round(2).replace({np.NAN: None}) 
# sql_Date_Value_12col(dbName, df)


# def sector_closePrice():
#     today = datetime.today()
#     todayOffset2 = today - dt.timedelta(14)
#     # todayOffset2 = datetime(1993, 5, 3)
    
#     # raw_data = web.DataReader('^GSPC', 'yahoo', datetime.datetime(2022, 2, 5), datetime.datetime(2022, 2, 6), api_key=None)
#     s5TELS = web.DataReader('^SP500-50', 'yahoo', todayOffset2, today, api_key=None)
#     s5COND = web.DataReader('^SP500-25', 'yahoo', todayOffset2, today, api_key=None)
#     s5CONS = web.DataReader('^SP500-30', 'yahoo', todayOffset2, today, api_key=None)

#     sPN     = web.DataReader('^GSPE', 'yahoo', todayOffset2, today, api_key=None)    
#     sPF     = web.DataReader('^SP500-40', 'yahoo', todayOffset2, today, api_key=None)
#     s5HLTH = web.DataReader('^SP500-35', 'yahoo', todayOffset2, today, api_key=None)
    
#     s5INDU = web.DataReader('^SP500-20', 'yahoo', todayOffset2, today, api_key=None)
#     s5INFT = web.DataReader('^SP500-45', 'yahoo', todayOffset2, today, api_key=None)
#     s5MATR = web.DataReader('^SP500-15', 'yahoo', todayOffset2, today, api_key=None)
    
#     s5UTIL = web.DataReader('^SP500-55', 'yahoo', todayOffset2, today, api_key=None)    
#     s5REAS = web.DataReader('^SP500-60', 'yahoo', todayOffset2, today, api_key=None)

#     s5TELS.reset_index(inplace=True) 
#     s5COND.reset_index(inplace=True) 
#     s5CONS.reset_index(inplace=True)
#     sPN.reset_index(inplace=True) 
#     sPF.reset_index(inplace=True) 
#     s5HLTH.reset_index(inplace=True)
#     s5INDU.reset_index(inplace=True) 
#     s5INFT.reset_index(inplace=True) 
#     s5MATR.reset_index(inplace=True)
#     s5UTIL.reset_index(inplace=True)    
#     s5REAS.reset_index(inplace=True)

#     s5TELS =s5TELS.sort_values(by= s5TELS.columns[0], ascending = False)
#     s5COND =s5COND.sort_values(by= s5COND.columns[0], ascending = False)
#     s5CONS =s5CONS.sort_values(by= s5CONS.columns[0], ascending = False)
#     sPN	   =sPN.sort_values(by= sPN.columns[0], ascending = False)
#     sPF	   =sPF.sort_values(by= sPF.columns[0], ascending = False)
#     s5HLTH =s5HLTH.sort_values(by= s5HLTH.columns[0], ascending = False)
#     s5INDU =s5INDU.sort_values(by= s5INDU.columns[0], ascending = False)
#     s5INFT =s5INFT.sort_values(by= s5INFT.columns[0], ascending = False)
#     s5MATR =s5MATR.sort_values(by= s5MATR.columns[0], ascending = False)
#     s5UTIL =s5UTIL.sort_values(by= s5UTIL.columns[0], ascending = False)   
#     s5REAS =s5REAS.sort_values(by= s5REAS.columns[0], ascending = False)
    
#     df = pd.DataFrame()
#     df['Date'] = s5TELS['Date']
#     df['s5TELS'] =s5TELS['Close']
#     df['s5COND'] =s5COND['Close']
#     df['s5CONS'] =s5CONS['Close']
#     df['sPN'] 	 =sPN['Close'] 
#     df['sPF'] 	 =sPF['Close'] 
#     df['s5HLTH'] =s5HLTH['Close']
#     df['s5INDU'] =s5INDU['Close']
#     df['s5INFT'] =s5INFT['Close']
#     df['s5MATR'] =s5MATR['Close']
#     df['s5UTIL'] =s5UTIL['Close']   
#     df['s5REAS'] =s5REAS['Close'] 
    
#     df = df.round(2).replace({np.NAN: None})    
#     # saveFileFullPath = _dir_sp500_value + 'sector_closePrice.csv'
#     # df.to_csv(saveFileFullPath, mode='a', index = False, header=False)
#     # df.round(2).to_csv(saveFileFullPath, index = False)
#     dbName = _sqlTable_SP500_ClosePrice_Sector
#     sql_Date_Value_12col(dbName, df)
#     print("SP500 11 sectors - close price downlaoded, sql") 
# # sector_closePrice() 
# # print()   



# def PE_shiller_multpl_shillerTotal():
#     url = 'https://www.multpl.com/shiller-pe/table/by-month'
#     saveFileFullPath = _dir_sp500_ratio + 'PE_Shiller_Multpl.csv'
    
#     list0 = pd.read_html(url) 
#     df1 = list0[0]
        
#     df = pd.DataFrame()
#     df['Date'] = pd.to_datetime(df1[df1.columns[0]] , format='%b %d, %Y') #	Date	May 14, 2021
#     df['Shiller'] = pd.to_numeric(df1[df1.columns[1]], errors='coerce')   
#     df = df.replace({np.NAN: None})    

#     #-- to csv file
#     df = df.sort_values(by = df.columns[0],  ascending=False)
#     df4 = df.head(1)
#     df4.to_csv(saveFileFullPath, mode='a', index = False, header=False)
    
#     #----sql
#     # df4 = pd.read_csv(saveFileFullPath)
#     dbName = _sqlTable_ratio_PEshiller
#     sql_Date_Value(dbName, df4)    
#     print("PE Shiller ratio downlaoded, sql")
# # PE_shiller_multpl_shillerTotal()

# def PE_TTM_Total_multpl():
#     url = 'https://www.multpl.com/s-p-500-pe-ratio/table/by-month'
    
#     saveFileFullPath = _dir_sp500_ratio + 'PE_TTM.csv'
    
#     list0 = pd.read_html(url) 
#     df3 = list0[0]
#     df2 = (df3[df3.columns[1]].str.split(' ',n=1, expand=True))
#     df1 = pd.DataFrame()
#     df1['Date'] = df3[df3.columns[0]].str.strip()
#     df1['Value'] = df2[df2.columns[0]].str.strip()
#     df = pd.DataFrame()
#     df['Date'] = pd.to_datetime(df1[df1.columns[0]] , format='%b %d, %Y') #	Date	May 14, 2021
#     df['PE_TTM'] = pd.to_numeric(df1[df1.columns[1]], errors='coerce')   
#     df = df.replace({np.NAN: None})    

#     #-- to csv file    
#     df = df.sort_values(by = df.columns[0],  ascending=False)
#     df4 = df.head(1)
#     # df4 = df
#     df4.to_csv(saveFileFullPath, mode='a', index = False, header=False)
    
#     #----sql
#     # df4 = pd.read_csv(saveFileFullPath)
#     dbName = _sqlTable_ratio_PE_TTM
#     sql_Date_Value(dbName, df4)    
#     print("PE 12 month trailing ratio downlaoded, sql")
# # PE_TTM_Total_multpl()
# # print()
    


# def extrac_sql_guru_shillerRatio2(csvFileFullPath, dbName, saveFileFullPath):
#     df1 = pd.read_csv(csvFileFullPath)
#     df2 = df1.dropna(how='all')    
#     df = df2.iloc[1:-1, :]
#     df.columns = df1.columns
    
#     df[df.columns[0]] = pd.to_datetime(df[df.columns[0]] , format='%Y-%m-%d')    
#     for col in  df.columns[2:]:
#         df[col] = pd.to_numeric(df[col], errors='coerce')#,downcast= 'integer') 
    
#     # a = df.columns[0]
#     df = df.replace({np.NAN: None})    
#     df = df.sort_values(by = df.columns[0],  ascending=False)

#     df.to_csv(saveFileFullPath, index = False)    
# #-------sql---------------------    
#     cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server+';DATABASE='+_database+';UID='+_username+';PWD='+_password)
#     cursor = cnxn.cursor()      
# #*****quick update*********************    
#     df = df.head(5)
# #******************************
#     for colName, coldata in df.iteritems():
#         if 'unnamed' in colName.lower():
#             pass
#         else:
#             sectorName = colName
#             i = df.columns.get_loc(colName)
#             # rows = 1 to last, col sector + 1
#             df_data = df.iloc[ : , [0, i, i+1]]
#             df_data.insert(1, 'Sector', sectorName)
#             df_data[df_data.columns[1]] = df_data[df_data.columns[1]].str.slice(0,21)           
#             print(sectorName)
            
#             for index, row in df_data.iterrows():
#                 #----comment out for fast operation-----
#                 dateStr = row[0]     
#                 query = """DELETE FROM %s where Date = '%s' and [Sector] = '%s' and [ShillerPE] = %s and [RegulaPE] = %s ;""" % (dbName, dateStr, row[1], row[2], row[3])
#                 cursor.execute(query) 
                
#                 params = tuple(row)
#                 query = """INSERT INTO %s VALUES (?,?,?,? );""" %(dbName)
#                 cursor.execute(query, params)                 
#     cnxn.commit()        
#     cursor.close()
#     cnxn.close()             
# csvFileFullPath = myguruShiller.SP500_Ratios_dir_ShillerPE +'/GuruFocus_Sector_Shiller_PE_Historical_Data.xls.csv'
# dbName = _sqlTable_SP500_Ratios_daily_sector_shillerPE
# saveFileFullPath = myguruShiller.SP500_Ratios_dir_PE + '/guru_sp500_PE_SectorShiller_dailyUpdated.csv'
# extrac_sql_guru_shillerRatio2(csvFileFullPath, dbName, saveFileFullPath)

# def excel_to_CSV_guru(fileFullPath):     
#     fileAbsPath = os.path.abspath(fileFullPath)   
#     winPath = fileAbsPath.replace(os.sep,ntpath.sep)   
#     xlApp = win32com.client.Dispatch('Excel.Application')
#     xlApp.Visible = False
#     xls = xlApp.Workbooks.Open(winPath)

#     csvFileFullPath = winPath+".csv"
#     if os.path.isfile( csvFileFullPath):
#         os.remove( csvFileFullPath)
#         print('file removed: ' + fileFullPath)    
#     xls.SaveAs( csvFileFullPath, FileFormat=6)
#     # xls.close()
#     xlApp.quit()
#     return csvFileFullPath
# fileFullPath = myguruShiller.SP500_Ratios_dir_ShillerPE +'/GuruFocus_Sector_Shiller_PE_Historical_Data.xls'
# csvFileFullPath = excel_to_CSV_guru(fileFullPath)    
# print(csvFileFullPath)  

#-------donwload files-------------------------------
# def downloadExcelFile(targetDir, fileName, webAddress):
#     # makeTodayDataDir(targetDir)    
#     newFilefullPath = targetDir + '/' + fileName
    
#     if os.path.isfile(newFilefullPath):
#         os.remove(newFilefullPath)
#         print('file removed: ' + newFilefullPath)    
    
#     headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3"}
#     # reg_url = url
#     req = Request(url = webAddress, headers = headers) 
#     html = urlopen(req).read()  
#     with open(newFilefullPath, 'wb') as outfile:
#         outfile.write(html)   
    
#     print('Downloaded Guru sp500 shillerPE daily: ' + newFilefullPath)
#     return newFilefullPath

# def guru_sp500_PE_shillerSector_daily():    
#     targetDir = myguruShiller.SP500_Ratios_dir_ShillerPE 
#     fileName = datetime.today().strftime('%Y-%m-%d') +'_' + 'GuruFocus_Sector_Shiller_PE_Historical_Data.xls'
#     webAddress = myguruShiller._Guru_shillerSector_URL
    
#     newExcel_FilefullPath = downloadExcelFile(targetDir, fileName, webAddress)
#     csvFileFullPath = excel_to_CSV_guru(newExcel_FilefullPath)
    
#     # csvFileFullPath = myguruShiller.SP500_Ratios_dir_ShillerPE +'/GuruFocus_Sector_Shiller_PE_Historical_Data.xls.csv'
#     dbName = _sqlTable_SP500_Ratios_daily_sector_shillerPE
#     saveFileFullPath = myguruShiller.SP500_Ratios_dir_PE + '/guru_sp500_PE_SectorShiller_dailyUpdated.csv'
#     extrac_sql_guru_shillerRatio2(csvFileFullPath, dbName, saveFileFullPath)
 
# # guru_sp500_PE_shillerSector_daily()
    


