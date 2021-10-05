# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 13:15:30 2021

http://www.kitconet.com/


@author: haoli
"""


import sys
sys.path.append("../")
import const_common as constA
import Const_NYMEXCOMEX_A as constCOMEX_A

# import requests
from os import makedirs
import os.path as myPath
import pandas as pd

# from urllib.request import urlopen, Request
# from pathlib import Path 
from datetime import datetime

import os

# import pyodbc
# import numpy as np

import time
from selenium import webdriver

import ntpath
#----------------------------------
errorFileTargetDir = '../'

# mydownPy.logError("my test message")
#logError(errorFileTargetDir, msg)
# mydownPy.logError(errorFileTargetDir, "my test message")

import key as pconst
_server = pconst.RYAN_SQL['server']
_database = pconst.RYAN_SQL['database']
_username = pconst.RYAN_SQL['username']
_password = pconst.RYAN_SQL['password']    

pd.set_option('mode.chained_assignment', None)

#--------table name ---------
_sqlTable_COMEX_stock = 'COMEX_Stock'     

_sqlTable_COMEX_Daily_Report_OpenInterest_LongShortPositon = 'COMEX_Daily_Report_OpenInterest_LongShortPositon' 

"""

"""
def makeTodayDataDir(newDir):
    # if not myPath.lexists(newDir): #lexists
    if not myPath.exists(newDir):
        makedirs(newDir)
        

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
# keyword = ''
# a = getDateFromString(dateStr, keyword)  
# print(a) 



def download_webpageReport_Files_2(save_toDataDir, comexWebsite_List):
    makeTodayDataDir(save_toDataDir) 
    
    fileAbsPath = os.path.abspath(save_toDataDir)   
    winPath = fileAbsPath.replace(os.sep,ntpath.sep)
    prefs = {"download.default_directory" : winPath,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing_for_trusted_sources_enabled": False,
            "safebrowsing.enabled": False,            
            'download.manager.showWhenStarting': False,
            'helperApps.neverAsk.saveToDisk': 'text/csv/xls, application/vnd.ms-excel, application/octet-stream'
             }  #("network.http.response.timeout", 30)     
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome('chromedriver.exe', options = chromeOptions)  # Optional argument, if not specified will search path.
    time.sleep(1) 
    
    for i in range(len(comexWebsite_List)): 
        url = comexWebsite_List[i][1]      
        driver.get(url)
        time.sleep(1)
        
    driver.quit()
    time.sleep(1)
        

def COMEX_gainStock_Tuesday_weekly_Run():
    save_toDataDir = constCOMEX_A.CME_gainStock_Tuesday_dir + '/' + constA.todayDate_str
    comexWebsite_List =  constCOMEX_A.comexWebsite_gainStock_Tuesday_List
    download_webpageReport_Files_2(save_toDataDir, comexWebsite_List)
COMEX_gainStock_Tuesday_weekly_Run()


def COMEX_bondsFuture_Delivered_Q_Run():
    save_toDataDir = constCOMEX_A.CME_bonds_dilivered_Q + '/' + constA.todayDate_str
    comexWebsite_List =  constCOMEX_A.comexWebsite_bondsDelivered_Q_List
    download_webpageReport_Files_2(save_toDataDir, comexWebsite_List)
# COMEX_bondsFuture_Delivered_Q_Run()



















