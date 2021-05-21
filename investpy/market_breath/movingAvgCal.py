import pandas as pd
# from pandas_datareader import data
import os.path as myPath
from datetime import date, datetime, timedelta
# import os

##########constant

todayDate_str = datetime.today().strftime('%Y-%m-%d') 
todayDateOffset_str = ( datetime.today() + timedelta(days=-720) ).strftime('%Y-%m-%d')  
now_str = str(datetime.now())

errorTxtfileName_const = todayDate_str + ' errorlog.txt'

sp500dataWorkingDir_const = "./sp500_data"
sp500Info_file_const = "SP500-info.csv"
sp500dataPrepDir_const    = "./sp500_prepData"

#------------------ 
# sp500dataDir2006_const = "./sp500History/2006"
# sp500dataDir2012_const = "./sp500History/2012"
# sp500dataDir2020_const = "./sp500History/2020"
# endDate2006_const = "2006-01-01"
# endDate2012_const = "2012-01-01"
# endDate2020_const = "2020-01-01"
sp500HisFile_list_const = [ ["2006-01-01", "./sp500History/2006"], 
               ["2012-01-01", "./sp500History/2012"],
               ["2020-01-01", "./sp500History/2020"] ]

#------------------------------

def calMovingAvg_tick(sourceFillpath, targetDir, ticker):
    tragetFillFullpath = targetDir + "/" + ticker + ".csv "    
    if myPath.isfile(sourceFillpath):
        dftemp = pd.DataFrame()
        df = pd.read_csv(sourceFillpath, parse_dates=['Date'], index_col='Date')        
        # df.set_index('Date', inplace = True)
        
        #Date,High,Low,Open,Close,Volume,Adj Close        
        dftemp['Close'] = df['Close']
        dftemp['Volume'] = df['Volume']
        dftemp['MA5']  = df['Close'].rolling(window=5).mean()
        dftemp['MA10'] = df['Close'].rolling(window=10).mean()
        dftemp['MA30'] = df['Close'].rolling(window=30).mean()
        dftemp['MA60'] = df['Close'].rolling(window=60).mean()
        dftemp['MA120'] = df['Close'].rolling(window=120).mean()
        dftemp['MA200'] = df['Close'].rolling(window=200).mean()        
        dftemp.to_csv(tragetFillFullpath,  float_format='%.3f')
    else:
        print ("\nMoving avg error - tickers file does not exist: " + ticker)
    
# ticker = "TSM"
# sourceFillpath = "./sp500_data/TSM.csv"

# panel_data = data.DataReader(name = ticker, data_source='yahoo', start='2021-01-05', end='2021-01-10')
# panel_data.to_csv("test3.csv")
# pd3 = pd.read_csv("test3.csv", index_col='Date')
# pd3.set_index('Date',inplace = True)

# calMovingAvg_tick(sourceFillpath, sp500dataPrepDir_const, ticker)
    
def CalMovingAvg_list(filePath_with_SymbolCol, src_Dir, dest_Dir):
    if myPath.isfile(filePath_with_SymbolCol):
        df = pd.read_csv(filePath_with_SymbolCol)  
        for ticker in df['Symbol']: 

            filename = ticker + ".csv"
            srcfillFullpath = src_Dir +"/" + filename            
            if myPath.isfile(srcfillFullpath):                
                calMovingAvg_tick(srcfillFullpath, dest_Dir, ticker)
                # print(" no thing")                
            else:  #new stock input and download history 
                print ("\nStock file does not exist, cannot cal MA: " + srcfillFullpath)
    else:
        print ("\nSP 500 tickers file does not exist")
        
def overwrite_sp500_prepDirFiles():        
    CalMovingAvg_list(filePath_with_SymbolCol=sp500Info_file_const, 
                      src_Dir = sp500dataWorkingDir_const, 
                      dest_Dir = sp500dataPrepDir_const)    
    
# >>> xlsx = pd.ExcelFile('file.xls')
# >>> df = pd.read_excel(xlsx,  'Sheet1')        