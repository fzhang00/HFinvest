# -*- coding: utf-8 -*-
"""
Created on Sat Mar 13 10:25:05 2021

@author: haoli
"""
"""
installed package:  seaborn, pandas_datareader


"""
# import pandas as pd
# from pandas_datareader import data
# import os.path as myPath
from datetime import datetime, timedelta

##########constant
todayDate_str = datetime.today().strftime('%Y-%m-%d') 
todayDateOffset_str = ( datetime.today() + timedelta(days=-720) ).strftime('%Y-%m-%d')  
now_str = str(datetime.now())
errorTxtfileName_const = todayDate_str + ' errorlog.txt'


#-----------------------
sp500Info_file_const = "SP500-info.csv"


sp500dataWorkingDir_const   = "./sp500_data"
sp500_sectorsDir_const      = "./sp500_sectors"
sp500_sectorsDir_tempConst      = "./sp500_sectors/temp"
sp500_sectorsDir_marketBreadthConst      = "./sp500_sectors/market_breadth"

sp500dataPrepDir_const      = "./sp500_prepData"

# sp500_ratiosDir_const      = "./sp500_ratios"
sp500_ratiosFillPath_const      = "./sp500_ratios/sp500ratios.csv"

shillerPE_FillPath_const      = "./sp500_ratios/ShillerPE.xls"

#------------------------
sp500Ratios_quandlList = [["INFLADJprice","MULTPL/SP500_INFLADJ_MONTH"],
["REAL_PRICE","MULTPL/SP500_REAL_PRICE_MONTH"],

["PE","MULTPL/SP500_PE_RATIO_MONTH"],
["SHILLER_PE","MULTPL/SHILLER_PE_RATIO_MONTH"],

["EARNINGS","MULTPL/SP500_EARNINGS_MONTH"],
["EARNINGS_GROWTH_Q","MULTPL/SP500_EARNINGS_GROWTH_QUARTER"],
["REAL_EARNINGS_GROWTH_Q","MULTPL/SP500_REAL_EARNINGS_GROWTH_QUARTER"],

["EARNINGS_YIELD","MULTPL/SP500_EARNINGS_YIELD_MONTH"],

["DIV","MULTPL/SP500_DIV_MONTH"],
["DIV_GROWTH_Q","MULTPL/SP500_DIV_GROWTH_QUARTER"],
["DIV_YIELD","MULTPL/SP500_DIV_YIELD_MONTH"],

["PSR_Q","MULTPL/SP500_PSR_QUARTER"], #sales
["SALES_Q","MULTPL/SP500_SALES_QUARTER"],
["SALES_GROWTH_Q","MULTPL/SP500_SALES_GROWTH_QUARTER"],

["REAL_SALES_Q","MULTPL/SP500_REAL_SALES_QUARTER"],
["REAL_SALES_GROWTH_Q","MULTPL/SP500_REAL_SALES_GROWTH_QUARTER"],

["PBV_Q","MULTPL/SP500_PBV_RATIO_QUARTER"],
["BVPSshare_Q","MULTPL/SP500_BVPS_QUARTER"]] #book value share

#------------------------
quandlData_const = 'quandl' 
quandlKey_const = '_JyFt8HS_T8C4qsXBo68'





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

#---------------------



