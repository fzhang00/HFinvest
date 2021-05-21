# -*- coding: utf-8 -*-
import pandas as pd
import os.path as myPath

from pandas_datareader import data
from datetime import datetime
import sp500Const as const
# import os

##########constant
# #------------------ 
# # sp500dataDir2006_const = "./sp500History/2006"
# # sp500dataDir2012_const = "./sp500History/2012"
# # sp500dataDir2020_const = "./sp500History/2020"
# # endDate2006_const = "2006-01-01"
# # endDate2012_const = "2012-01-01"
# # endDate2020_const = "2020-01-01"

pause_downloadrequest = 30 # in seconds
yahooDATA_const = 'yahoo' 
quandlData_const = 'quandl' 
quandlKey_const = '_JyFt8HS_T8C4qsXBo68'

#------------------------

# sp500_ratiosFillPath_const   sp500Ratios_quandlList

#------------------------------
historyStart_date  = '1970-01-01'   
start_date = '1999-01-01'#datetime(2021, 1, 5) #'2020-01-01'
end_date   = const.todayDate_str #datetime(2021, 3, 27)#'2020-12-31'

# panel_data = data.DataReader(name = "MULTPL/SP500_HISTORICAL_PRICE", data_source = quandlData_const, start=historyStart_date, end=end_date, api_key=quandlKey_const)
# print (panel_data)

#----functions
def downloadSP500HistoryRatios(dataSource, historyStart_date, downloadList, api_key, targetFillPath): 
    #api_key=None 
    start_date = historyStart_date
    # end_date   = const.todayDate_str
    df = pd.DataFrame(columns = ['Date'] ) 
    df.set_index('Date', inplace = True)
              
    if myPath.isfile(targetFillPath):
        print ("\nfile exist, update the last rows based on time")
        dfOldFile = pd.read_csv(targetFillPath, parse_dates=['Date'], index_col='Date') #parse_dates=['Date'],      
        lastRowDate = dfOldFile.index[-1] #  tail(1)['Date']
        # lastRowDate = dfOldFile.iloc[-1]['Date'] #dfOldFile.iloc[-1][0]
        
        dfOldFile.drop(dfOldFile.tail(1).index, inplace=True)
        # print(dfOldFile.tail(1))                
        start_date = (lastRowDate).strftime('%Y-%m-%d')             
    else:
        print ("\ndonothing")
        dfOldFile = df # empty dfOldFile
        
    for i in range(len(downloadList)): 
        colName = downloadList[i][0]
        sourceSourceLinkName = downloadList[i][1]            
        panel_data = data.DataReader(name = sourceSourceLinkName, data_source = quandlData_const, 
                                     start=start_date, end=end_date, api_key=api_key)   
        
        panel_data[colName] = panel_data[panel_data.columns[-1]]
        # # df[df.columns[-1]]  df.iloc[:,-1:]  pd_csv.iloc[:,-1:]      
        df = pd.DataFrame.join(df, panel_data[colName], how='outer')    
    
    df = dfOldFile.append(df)    
    df.to_csv(targetFillPath, float_format='%.2f')
# testing call        
# downloadSP500HistoryRatios(dataSource = quandlData_const, historyStart_date = historyStart_date, 
#                           downloadList = const.sp500Ratios_quandlList, api_key= quandlKey_const, 
#                           targetFillPath= const.sp500_ratiosFillPath_const)    
    
def getDataFrame_tick(sourceFillpath, ticker):
    df = pd.DataFrame()
    if myPath.isfile(sourceFillpath):
        df = pd.read_csv(sourceFillpath, parse_dates=['Date'], index_col='Date')               
    else: # log the error
        print ("\ntickers file does not exist: " + ticker)
        if myPath.exists(const.errorTxtfileName_const):
            append_write = 'a' # append if already exists
        else:
            append_write = 'w' # make a new file if not        
        f = open(const.errorTxtfileName_const, append_write)
        f.write('\n'+const.now_str + "ticker file does not exist: " + ticker)
        f.close()       
    return df 


def load_historyDataFrame (ticker, sp500HisInfo_list):
    filename = ticker + ".csv" 
    df = pd.DataFrame()
    # df = pd.DataFrame(list())
    for i in range(len(sp500HisInfo_list)):  
        fillFullpath = sp500HisInfo_list[i][1] +"/" + filename        
        if myPath.isfile(fillFullpath):
            dftemp = pd.read_csv(fillFullpath, parse_dates=['Date'], index_col='Date')
            df = df.append(dftemp)
    #remove duplicate and sort by date 
            df.drop_duplicates()
            df = df.sort_values(['Date'])
            #print(dftemp.head(1))
            # df_old.drop_duplicates(subset=None, inplace=True)            
            # df_old.reset_index().drop_duplicates('Date').set_index('Date')
            # df1 = df_old[~df_old.index.duplicated(keep='last')]              
    return df 

    

def download_StockPrice(ticker, dataSource, start_date, end_date):
    try:
        if pause_downloadrequest <= 1:
            panel_data = data.DataReader(name = ticker, data_source = dataSource, start=start_date, end=end_date)
        else:
            panel_data = data.DataReader(name = ticker, data_source = dataSource, start=start_date, end=end_date,pause=pause_downloadrequest)
        # panel_data1 = panel_data.to_csv("test.csv")
        return panel_data
    except Exception as ex:
        # try google finance api
        #https://clu.gitbook.io/python-web-crawler-note/44-google-finance-api 
        
        print(const.now_str + "  "+ str(ticker) + '  stock price download Error:', ex)        
        if myPath.exists(const.errorTxtfileName_const):
            append_write = 'a' # append if already exists
        else:
            append_write = 'w' # make a new file if not        
        f = open(const.errorTxtfileName_const, append_write)
        f.write('\n'+const.now_str + '  SP500 download error - %s' + ticker + ' - '+ str(start_date) + ' - '+ str(end_date))
        f.close()
        return pd.DataFrame(list())
        #continue

def download_Save_StockPrice (ticker, fillFullpath, start_date, end_date):
    df = download_StockPrice(ticker, yahooDATA_const, start_date, end_date)
    if not df.empty:
        df = df.to_csv(fillFullpath, float_format='%.3f')
        print ("downloaded and saved a file "+ fillFullpath)
        
        
        

def download_Save_HistoryData (ticker, start_date, sp500HisInfo_list):
    filename = ticker + ".csv"
    for i in range(len(sp500HisInfo_list)):
        # print(sp500HisInfo_list[i][0]) 2006-01-01
        # print(sp500HisInfo_list[i][1]) ./sp500History/2006    
        fillFullpath = sp500HisInfo_list[i][1] +"/" + filename
        if myPath.isfile(fillFullpath):
            print ("\nfile exist, no data overwirite: " + fillFullpath)
        else:
            end_date = sp500HisInfo_list[i][0]
            if i == 0:
                download_Save_StockPrice(ticker, fillFullpath, start_date, end_date)
            else:
                start_date = sp500HisInfo_list[i-1][0]
                download_Save_StockPrice(ticker, fillFullpath, start_date, end_date)
            print ("\ncreat a new history file "+ fillFullpath)
            
def update_workingData(ticker, fillFullpath):
    dfOldFile = pd.read_csv(fillFullpath, parse_dates=['Date'], index_col='Date') #parse_dates=['Date'],
               
    lastRowDate = dfOldFile.index[-1] #  tail(1)['Date']
    # lastRowDate = dfOldFile.iloc[-1]['Date'] #dfOldFile.iloc[-1][0]
    
    dfOldFile.drop(dfOldFile.tail(1).index, inplace=True)
    # print(dfOldFile.tail(1))
        
    start_date = (lastRowDate).strftime('%Y-%m-%d')    
    end_date = const.todayDate_str
    
    panel_data1 = download_StockPrice(ticker, yahooDATA_const, start_date, end_date)   
    
    if not panel_data1.empty:
        df3 = pd.concat([dfOldFile, panel_data1])#, ignore_index=True ) 
        df3.to_csv(fillFullpath,  float_format='%.3f')
        print ("\nstock updated today: " + end_date + " - "+ ticker)
    else:
        print ("\nNo update data today: " + end_date + " - "+ ticker)

def download_Update_SaveData_History_all500 (sp500info_file, start_date, sp500HisInfo_list, sp500dataWorkingDir):
    if myPath.isfile(sp500info_file):
        df = pd.read_csv(sp500info_file)
        
        for ticker in df['Symbol']:
            filename = ticker + ".csv"
            fillFullpath = sp500dataWorkingDir +"/" + filename
            
            if myPath.isfile(fillFullpath):
                update_workingData(ticker, fillFullpath)                 
            else:  #new stock input 
                #download history 
                download_Save_HistoryData (ticker, start_date, sp500HisInfo_list)                
                # download to working dir 
                download_Save_StockPrice (ticker, fillFullpath, const.todayDateOffset_str, const.todayDate_str)
                
    else:
        print ("\nSP 500 tickers file does not exist")
        
        
#------start of the code --------------------

if not myPath.exists(const.sp500dataWorkingDir_const):
    myPath.mkdir(const.sp500dataWorkingDir_const)
   
# download_Update_SaveData_History_all500 (const.sp500Info_file_const, start_date, const.sp500HisFile_list_const, const.sp500dataWorkingDir_const)    





#--------testing -------------------------
# ticker = "TSM"
# dataPath = "./sp500_data/TSM.csv"
# update_workingData(ticker, dataPath)


#--------------------------
    
# #an empty dataframe    
# df1 = pd.DataFrame(list())

#---------------------------

# dftemp = dftemp.append(df)['Symbol'].drop_duplicates()
# d={}
# d = dftemp.append(df)['Symbol'].unique()


# >>> os.path.isfile("/etc/password.txt")
# True
# >>> os.path.isfile("/etc")
# False
# >>> os.path.isfile("/does/not/exist")
# False
# >>> os.path.exists("/etc/password.txt")
# True
# >>> os.path.exists("/etc")
# True
# >>> os.path.exists("/does/not/exist")

# df2.loc[0, "col1"] = "c"
# len(df.columns)


# import pandas
# colnames = ['year', 'name', 'city', 'latitude', 'longitude']
# data = pandas.read_csv('test.csv', names=colnames)
# If you want your lists as in the question, you can now do:
# names = data.name.tolist()