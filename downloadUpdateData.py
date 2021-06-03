# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 21:29:13 2021

@author: haoli
"""
import requests
import pandas as pd

import const_common as const
from pandas_datareader import data

import os.path as myPath
from pathlib import Path
import glob
    # name,
    # data_source=None,
    # start=None,
    # end=None,
    # retry_count=3,
    # pause=0.1,
    # session=None,
    # api_key=None,

"""
return dataFrame is data is downloaded
or a empty dataFrame

api_key = None if no key
"""
def logError(msg):
    if myPath.exists(const.errorTxtfileName_const):
        append_write = 'a' # append if already exists
    else:
        append_write = 'w' # make a new file if not        
    f = open(const.errorTxtfileName_const, append_write)
    f.write('\n'+const.now_str + '  error - ' + msg )
    f.close() 
    
def logError(errorFileTargetDir, msg):
    fillPath = errorFileTargetDir + '/' + const.errorTxtfileName_const
    if myPath.exists(fillPath):
        append_write = 'a' # append if already exists
    else:
        append_write = 'w' # make a new file if not        
    f = open(fillPath, append_write)
    f.write('\n'+const.now_str + '  error - ' + msg )
    f.close()
    
def downloadWebsiteTables_returnDataFrameList(url):
    r = requests.get(url, allow_redirects=True)
    myDataFrameList = pd.read_html(r.content)  
    return myDataFrameList



def download_data(ticker, data_source, start_date, end_date, api_key):
    try:
        if const.pause_downloadrequest <= 1:
            panel_data = data.DataReader(name = ticker, data_source = data_source, start=start_date, end=end_date, api_key = api_key)
        else:
            panel_data = data.DataReader(name = ticker, data_source = data_source, start=start_date, end=end_date,pause=const.pause_downloadrequest, api_key = api_key)
        # panel_data1 = panel_data.to_csv("test.csv")
        panel_data.index.name = 'Date'
        return panel_data
    except Exception as ex:
        # try google finance api
        #https://clu.gitbook.io/python-web-crawler-note/44-google-finance-api 
        
        print(const.now_str + "  "+ str(ticker) + '  data download Error:', ex)        
        if myPath.exists(const.errorTxtfileName_const):
            append_write = 'a' # append if already exists
        else:
            append_write = 'w' # make a new file if not        
        f = open(const.errorTxtfileName_const, append_write)
        f.write('\n'+const.now_str + '  download error - %s' + ticker + ' - '+ str(start_date) + ' - '+ str(end_date))
        f.close()
        return pd.DataFrame(list())
        #continue
"""
download and overWrite data to a target fill directory
api_key = None if no key
"""
def download_overWrite_Data_toPath(ticker, data_source, start_date, end_date, api_key, targetFillFullpath):
    df = download_data(ticker, data_source, start_date, end_date, api_key)
    if not df.empty:
        df = df.to_csv(targetFillFullpath, float_format='%.3f')
        print ("downloaded and overwrite a file "+ targetFillFullpath)
"""
download and update data to a target fill directory
api_key = None if no key
"""        
def download_update_Data_toPath(ticker, data_source, start_date, end_date, api_key, targetFillFullpath):
    targetFillPath = targetFillFullpath
    
    df = pd.DataFrame(columns = ['Date'] ) 
    df.set_index('Date', inplace = True)
    
    if myPath.isfile(targetFillPath):
        
        try:
            dfOldFile = pd.read_csv(targetFillPath, parse_dates=['Date'], index_col=['Date']) #parse_dates=['Date'],      
            print ("\nfile exist, update the last rows based on time")

            # dfOldFile = pd.read_csv(targetFillPath, parse_dates=['Date'], index_col=['Date']) #parse_dates=['Date'],      
            dfOldFile =dfOldFile.sort_values(['Date'])
            lastRowDate = dfOldFile.index[-1] #  tail(1)['Date']
            # lastRowDate = dfOldFile.iloc[-1]['Date'] #dfOldFile.iloc[-1][0]
            
            dfOldFile.drop(dfOldFile.tail(1).index, inplace=True)
            # print(dfOldFile.tail(1))                
            start_date = (lastRowDate).strftime('%Y-%m-%d')             
            
            
        except Exception as ex:
            print(const.now_str + "  "+ str(ticker) + '  open file by date Error:', ex)        
            if myPath.exists(const.errorTxtfileName_const):
                append_write = 'a' # append if already exists
            else:
                append_write = 'w' # make a new file if not        
            f = open(const.errorTxtfileName_const, append_write)
            f.write('\n'+const.now_str + '  download error - %s' + ticker + ' - '+ str(start_date) + ' - '+ str(end_date))
            f.close()        
            dfOldFile = df # empty dfOldFile
    else:
        # print ("\ndonothing")
        dfOldFile = df # empty dfOldFile

    df = download_data(ticker, data_source, start_date, end_date, api_key)
    
    if not df.empty:
        df = dfOldFile.append(df)
        df = df.to_csv(targetFillFullpath, float_format='%.3f')
        print ("downloaded and update a file "+ targetFillFullpath)

"""
List is the 2d array with newfillName and ticker  
api_key = None if no key
"""        
def download_update_Data_byTicker_FillName_List(fillNameTicker_List, targetDir, data_source, start_date, end_date, api_key):
    
    df = pd.DataFrame(columns = ['Date'] ) 
    df.set_index('Date', inplace = True)
    
    for i in range(len(fillNameTicker_List)): 
        fileName = fillNameTicker_List[i][0] + ".csv" 
        targetFillFullpath = targetDir + "/" + fileName        
        
        ticker = fillNameTicker_List[i][1]
        
        download_update_Data_toPath(ticker, data_source, start_date, end_date, api_key, targetFillFullpath)

"""
isCopyCol = True direct adding the cols to the dataFrame
isCopyCol = False, use file name as the col name to attach 
return dataFrame
"""    
def combineFill_byDir(sourceFillDir, targetFillPath, isCopyCol):    
    df_temp = pd.DataFrame(columns = ['Date'] ) 
    df_temp.set_index('Date', inplace = True)
    
    files = glob.glob(sourceFillDir + "/*.csv")  
    for f in files:
        
        # pd_csv = pd.read_csv(f, index_col='Date')
        pd_csv = pd.read_csv(f)
        pd_csv.set_index(pd_csv.columns[0], inplace = True)
        pd_csv.index.name = 'Date'        
        
        if isCopyCol: #direct copy    
            df_temp = pd.DataFrame.join(df_temp, pd_csv, how='outer')            
        else: # use file name as the col name
            colName = Path(f).stem 
            # copy the first col to the new col name  
            #first_column = df. iloc[:, 0], df[df.columns[-1]]  df.iloc[:,-1:]  pd_csv.iloc[:,-1:] 
            pd_csv[colName] = pd_csv[pd_csv.columns[0]]
 
            df_temp = pd.DataFrame.join(df_temp, pd_csv[colName], how='outer')
    return df_temp   

#--------------------------------
def appendNewDataToFile_KeepLast(targetFile, df_data_noKey):
    df = pd.read_csv(targetFile)
    df.append()
    




        