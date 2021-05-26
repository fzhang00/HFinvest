# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 13:15:30 2021

http://www.kitconet.com/


@author: haoli
"""

FINRA_Dir_MarginStatistics = "./investpy/FINRA/MarginStatistics"

# commodityLMEDir         = commodityDir + "/LME"      #"./data/LME"
# # commodityLME_workDir    = commodityLMEDir  + "/temp" #"./data/LME/temp"
# commodityLME_workDir_A    = commodityLMEDir  + "/temp_A" #"./data/LME/temp"



_FINRA_MarginStatistics_URL = 'https://www.finra.org/investors/learn-to-invest/advanced-investing/margin-statistics'






#-----------------------------------------------

KEY_NONFERROUS = 'NONFERROUS' 
KEY_GOLD = 'Gold' 
KEY_SILVER = 'Silver'  

_NONFERROUS_FILENAME = 'nonFerrous_price_stock.csv'
_GOLD_FILENAME = "gold_price_vol_OI.csv"
_SILVER_FILENAME = "silver_price_vol_OI.csv"

_NONFERROUS_PRICE_STOCK_URL = 'https://www.lme.com/Metals/Non-ferrous'
_GOLD_PRICE_VOL_OI_URL     = "https://www.lme.com/Metals/Precious-metals/LME-Gold"
_SILVER_PRICE_VOL_OI_URL   = "https://www.lme.com/Metals/Precious-metals/LME-Silver"


DICT_URL_A = {KEY_NONFERROUS : _NONFERROUS_PRICE_STOCK_URL, KEY_GOLD : _GOLD_PRICE_VOL_OI_URL, KEY_SILVER  : _SILVER_PRICE_VOL_OI_URL }
DICT_URL_A_FILENAME = { KEY_NONFERROUS : _NONFERROUS_FILENAME,  KEY_GOLD : _GOLD_FILENAME, KEY_SILVER : _SILVER_FILENAME }

#-------daily volume-----------------------
# commodityLME_dailyVolumeDir     = commodityDir  + "/LME_Volume_Daily" 
dialyVolume_url      = 'https://www.lme.com/LME-Clear/Technology/Reports/Volumes'


#---------------- weekly trader report----------

# commodityLME_trderReportDir  = commodityDir + "/LME_TraderReport" 
# trderReport_ALDir = commodityLME_trderReportDir +'/Aluminium'
# trderReport_CADir = commodityLME_trderReportDir +'/Copper'
# trderReport_goldDir = commodityLME_trderReportDir +'/Gold'
# trderReport_silverDir = commodityLME_trderReportDir +'/Silver'

#https://www.lme.com/Market-Data/Reports-and-data/Commitments-of-traders#tabIndex=0
ALTraderReport_url      = 'https://www.lme.com/en-GB/Market-Data/Reports-and-data/Commitments-of-traders/Aluminium'
CATraderReport_url      = 'https://www.lme.com/en-GB/Market-Data/Reports-and-data/Commitments-of-traders/Copper'
goldTraderReport_url    = 'https://www.lme.com/en-GB/Market-Data/Reports-and-data/Commitments-of-traders/Gold'
silverTraderReport_url  = 'https://www.lme.com/en-GB/Market-Data/Reports-and-data/Commitments-of-traders/Silver'



#-------daily Open interest-----------------------
# commodityLME_openInterestDir    = commodityDir  + "/LME_OpenInterest" 

# commodityLME_openInterestDir_base = commodityLME_openInterestDir + '/base_E' 
dialyOpenInterest_base_url      = 'https://www.lme.com/Market-Data/Reports-and-data/Open-interest/EOI'

# commodityLME_openInterestDir_precious = commodityLME_openInterestDir + '/precious_E'  
dialyOpenInterest_precious_url      = 'https://www.lme.com/Market-Data/Reports-and-data/Open-interest/EOI#tabIndex=1'


     
