# -*- coding: utf-8 -*-
"""
Created on Sat Mar 13 10:25:05 2021

@author: haoli
"""

from datetime import datetime, timedelta

import os
"""
    if num==0:
        return filePath
    elif num==1:
        return fileFullName
    elif num==2:
        return fileName
    elif num==3:
        return ext
"""
def getFilePathInfo (fullPath, num): 
    filePath, fileName_Ext = os.path.split(fullPath)    
    fileNameList = os.path.splitext(fileName_Ext)    
    fileName_NoExt = fileNameList[0]
    ext = fileNameList[1]
    
    if num==0:
        return filePath
    elif num==1:
        return fileName_Ext
    elif num==2:
        return fileName_NoExt
    elif num==3:
        return ext
    else:
        print ("Wrong choice to get file name")
        return "Wrong choice to get file name"        
    # print (filePath)
    # print (fileFullName)
    # print (fileName_NoExt)
    # print (ext)

# fullPath = "/tmp/d" # -> /tmp
# fullPath = 'London Metal Exchange_ LME Gold.csv.html'
# fullPath = "/tmp/2021-04-01" # 1 -> 2021-04-01
# print(getFilePathInfo(fullPath, 1)) 


def getDateFromString(dateStr, keyword): 
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
                print('9999')
                return d
    return date_fromFile.strftime('%Y-%m-%d')
# dateStr = 'Data valid for 500 April 2021 '
# keyword = 'Data valid for'
# dateStr = '01 Apr'
# keyword = ''
# a = getDateFromString(dateStr, keyword)  
# a = datetime.strptime('01 Apr', '%d %b') 
# s='01 Apr'
# a= datetime.strptime("{0} 2021".format(s), "%d %b %Y").strftime("%d-%m-%Y") 
# print(a) 

def convertDDMM_date(df, timeRef): # used for LME gold and silver
    yy = timeRef.split('-')
    year = yy[0]
    year1 = str(int(year) - 1) 
    #this line is for testing only
    # df['oldDate'] = df['Date'] # + ' ' + year 
    num = df.columns.get_loc('Date')    
    for i in range(len(df)): 
        dateStr = df.iloc[i][num] + ' ' + year 
        dateStr1 = df.iloc[i][num] + ' ' + year1 
        yy = datetime.strptime(dateStr, '%d %b %Y').strftime('%Y-%m-%d')
        if yy <= timeRef:
            df.iat[i, num] = yy
        else:
            yy = datetime.strptime(dateStr1, '%d %b %Y').strftime('%Y-%m-%d')        
            df.iat[i, num] = yy
    df.set_index('Date', inplace = True)    
    #     print()
    # print()
    return df
# import pandas as pd
# df = pd.read_csv('testFile_date.csv')
# timeRef = '2021-03-06' 
# convertDDMM_date(df, timeRef)

##########constant
todayDate_str = datetime.today().strftime('%Y-%m-%d') 
todayDateOffset_str = ( datetime.today() + timedelta(days=-720) ).strftime('%Y-%m-%d')
todayDateOffset_1D_str = ( datetime.today() + timedelta(days=-1) ).strftime('%Y-%m-%d')
  
now_str = str(datetime.now())
errorTxtfileName_const = todayDate_str + ' errorlog.txt'

  
#-----------------------

#------------------------
##########constant
pause_downloadrequest = 30 # in seconds
yahooDataSource_const = 'yahoo' 
quandlDataSource_const = 'quandl' 

