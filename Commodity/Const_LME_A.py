# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 13:15:30 2021

http://www.kitconet.com/


@author: haoli
"""

commodityDir = "./data"
commodityLMEDir         = commodityDir + "/LME"      #"./data/LME"
# commodityLME_workDir    = commodityLMEDir  + "/temp" #"./data/LME/temp"
commodityLME_workDir_A    = commodityLMEDir  + "/temp_A" #"./data/LME/temp"

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
commodityLME_dailyVolumeDir     = commodityDir  + "/LME_Volume_Daily" 
dialyVolume_url      = 'https://www.lme.com/LME-Clear/Technology/Reports/Volumes'


#---------------- weekly trader report----------

commodityLME_trderReportDir  = commodityDir + "/LME_TraderReport" 
trderReport_ALDir = commodityLME_trderReportDir +'/Aluminium'
trderReport_CADir = commodityLME_trderReportDir +'/Copper'
trderReport_goldDir = commodityLME_trderReportDir +'/Gold'
trderReport_silverDir = commodityLME_trderReportDir +'/Silver'

#https://www.lme.com/Market-Data/Reports-and-data/Commitments-of-traders#tabIndex=0
ALTraderReport_url      = 'https://www.lme.com/en-GB/Market-Data/Reports-and-data/Commitments-of-traders/Aluminium'
CATraderReport_url      = 'https://www.lme.com/en-GB/Market-Data/Reports-and-data/Commitments-of-traders/Copper'
goldTraderReport_url    = 'https://www.lme.com/en-GB/Market-Data/Reports-and-data/Commitments-of-traders/Gold'
silverTraderReport_url  = 'https://www.lme.com/en-GB/Market-Data/Reports-and-data/Commitments-of-traders/Silver'



#-------daily Open interest-----------------------
commodityLME_openInterestDir    = commodityDir  + "/LME_OpenInterest" 

commodityLME_openInterestDir_base = commodityLME_openInterestDir + '/base_E' 
dialyOpenInterest_base_url      = 'https://www.lme.com/Market-Data/Reports-and-data/Open-interest/EOI'

commodityLME_openInterestDir_precious = commodityLME_openInterestDir + '/precious_E'  
dialyOpenInterest_precious_url      = 'https://www.lme.com/Market-Data/Reports-and-data/Open-interest/EOI#tabIndex=1'



#------------------------------

# ALUMINATraderReport_url = 'https://www.lme.com/en-GB/Market-Data/Reports-and-data/Commitments-of-traders/Alumina'
# ALAlloyTraderReport_url = 'https://www.lme.com/en-GB/Market-Data/Reports-and-data/Commitments-of-traders/Aluminium-Alloy'
# ALmonthlyAvgFutureTraderReport_url = 'https://www.lme.com/en-GB/Market-Data/Reports-and-data/Commitments-of-traders/Aluminium-Monthly-Average-Futures'
# coppermonthlyAvgFutureTraderReport_url = 'https://www.lme.com/en-GB/Market-Data/Reports-and-data/Commitments-of-traders/Copper-Monthly-Average-Futures'
# leadTraderReport_url = 'https://www.lme.com/en-GB/Market-Data/Reports-and-data/Commitments-of-traders/Lead'
# leadmonthlyAvgFutureTraderReport_url = 'https://www.lme.com/en-GB/Market-Data/Reports-and-data/Commitments-of-traders/Lead-Monthly-Average-Futures'
# NASAACTraderReport_url = 'https://www.lme.com/en-GB/Market-Data/Reports-and-data/Commitments-of-traders/NASAAC'

# nickelTraderReport_url = 'https://www.lme.com/en-GB/Market-Data/Reports-and-data/Commitments-of-traders/Nickel'
# nickelmonthlyAvgFutureTraderReport_url = 'https://www.lme.com/en-GB/Market-Data/Reports-and-data/Commitments-of-traders/Nickel-Monthly-Average-Futures'

# tinTraderReport_url = 'https://www.lme.com/en-GB/Market-Data/Reports-and-data/Commitments-of-traders/Tin'
# tinmonthlyAvgFutureTraderReport_url = 'https://www.lme.com/en-GB/Market-Data/Reports-and-data/Commitments-of-traders/Tin-Monthly-Average-Futures'

# zincTraderReport_url = 'https://www.lme.com/en-GB/Market-Data/Reports-and-data/Commitments-of-traders/Zinc'
# zincmonthlyAvgFutureTraderReport_url = 'https://www.lme.com/en-GB/Market-Data/Reports-and-data/Commitments-of-traders/Zinc-Monthly-Average-Futures'



           
     


#--------------------------------------------



# -----------------------------not used

# LME_CuConst2 = ['Date', 'CUCash',	'CU3Month',	'CUDec22',	'CUOpenStock',	'CULiveWarrants',	'CUCancelledWarrants']
# LME_AlConst2 = ['Date', 'ALCash',	'AL3Month',	'ALDec22',	'ALOpenStock',	'ALLiveWarrants',	'ALCancelledWarrants']
# LME_ZnConst2 = ['Date', 'ZNCash',	'ZN3Month',	'ZNDec22',	'ZNOpenStock',	'ZNLiveWarrants',	'ZNCancelledWarrants']
# LME_NiConst2 = ['Date', 'NICash',	'NI3Month',	'NIDec22',	'NIOpenStock',	'NILiveWarrants',	'NICancelledWarrants']
# LME_LeadConst2 = ['Date', 'PBCash',	'PB3Month',	'PBDec22',	'PBOpenStock',	'PBLiveWarrants',	'PBCancelledWarrants']
# LME_TinConst2 =  ['Date', 'SNCash',	'SN3Month',	'SNDec22',	'SNOpenStock',	'SNLiveWarrants',	'SNCancelledWarrants']
# LME_AlAlloyConst2 = ['Date', 'AL_ALLOYCash',	'AL_ALLOY3Month',	'AL_ALLOYDec22',	'AL_ALLOYOpenStock',	'AL_ALLOYLiveWarrants',	'AL_ALLOYCancelledWarrants']
# LME_NASAACConst2  = ['Date', 'NASAACCash',	'NASAAC3Month',	'NASAACDec22',	'NASAACOpenStock',	'NASAACLiveWarrants',	'NASAACCancelledWarrants']





# LME_ListCost = [[LMECOPPERfileName,     "https://www.lme.com/en-GB/Metals/Non-ferrous/Copper#tabIndex=0"],
#                 [LMEALUMINIUMfileName,  "https://www.lme.com/en-GB/Metals/Non-ferrous/Aluminium#tabIndex=0"],
#                 [LMEZINCfileName,       "https://www.lme.com/Metals/Non-ferrous/Zinc#tabIndex=0"],
#                 [LMENICKELfileName,     "https://www.lme.com/Metals/Non-ferrous/Nickel#tabIndex=0"],
#                 [LMELEADfileName,       "https://www.lme.com/Metals/Non-ferrous/Lead#tabIndex=0"],
#                 [LMETINfileName,        "https://www.lme.com/Metals/Non-ferrous/Tin#tabIndex=0"],
#                 [LMEALUMINIUMALLOYfileName, "https://www.lme.com/Metals/Non-ferrous/Aluminium-Alloy#tabIndex=0"],
#                 [LMENASAACfileName,     "https://www.lme.com/Metals/Non-ferrous/NASAAC#tabIndex=0"]]

# LME_CuCol_Const = [LMECOPPERfileName,    'Date', 'CUCash',	'CU3Month',	'CUDec22',	'CUOpenStock',	'CULiveWarrants',	'CUCancelledWarrants']
# LME_AlCol_Const = [LMEALUMINIUMfileName, 'Date', 'ALCash',	'AL3Month',	'ALDec22',	'ALOpenStock',	'ALLiveWarrants',	'ALCancelledWarrants']
# LME_ZnCol_Const = [LMEZINCfileName,      'Date', 'ZNCash',	'ZN3Month',	'ZNDec22',	'ZNOpenStock',	'ZNLiveWarrants',	'ZNCancelledWarrants']
# LME_NiCol_Const = [LMENICKELfileName,   'Date', 'NICash',	'NI3Month',	'NIDec22',	'NIOpenStock',	'NILiveWarrants',	'NICancelledWarrants']
# LME_LeadCol_Const = [LMELEADfileName,   'Date', 'PBCash',	'PB3Month',	'PBDec22',	'PBOpenStock',	'PBLiveWarrants',	'PBCancelledWarrants']
# LME_TinCol_Const =  [LMETINfileName,    'Date', 'SNCash',	'SN3Month',	'SNDec22',	'SNOpenStock',	'SNLiveWarrants',	'SNCancelledWarrants']
# LME_AlAlloyCol_Const = [LMEALUMINIUMALLOYfileName, 'Date', 'AL_ALLOYCash',	'AL_ALLOY3Month',	'AL_ALLOYDec22',	'AL_ALLOYOpenStock',	'AL_ALLOYLiveWarrants',	'AL_ALLOYCancelledWarrants']
# LME_NASAACCol_Const  = [LMENASAACfileName,         'Date', 'NASAACCash',	'NASAAC3Month',	'NASAACDec22',	'NASAACOpenStock',	'NASAACLiveWarrants',	'NASAACCancelledWarrants']



# LME_nameListCost = ['CUCash', 'CU3Month', 'CUDec22',
#                     'ALCash', 'AL3Month', 'ALDec22',
#                     'ZNCash', 'ZN3Month', 'ZNDec22',
#                     'NICash', 'NI3Month', 'NIDec22',
#                     'PBCash', 'PB3Month', 'PBDec22',
#                     'SNCash', 'SN3Month', 'SNDec22',
#                     'AL_ALLOYCash', 'AL_ALLOY3Month',   'AL_ALLOYDec22',
#                     'NASAACCash',   'NASAAC3Month',     'NASAACDec22']

# LMECOPPER_url = "https://www.lme.com/en-GB/Metals/Non-ferrous/Copper#tabIndex=0"
# LMEAL_url = "https://www.lme.com/en-GB/Metals/Non-ferrous/Aluminium#tabIndex=0"
# LMEZINC_url = "https://www.lme.com/Metals/Non-ferrous/Zinc#tabIndex=0"
# LMENICKEL_url =     "https://www.lme.com/Metals/Non-ferrous/Nickel#tabIndex=0"
# LMELEAD_url =      "https://www.lme.com/Metals/Non-ferrous/Lead#tabIndex=0"
# LMETIN_url =       "https://www.lme.com/Metals/Non-ferrous/Tin#tabIndex=0"
# LMEALALLOY_url = "https://www.lme.com/Metals/Non-ferrous/Aluminium-Alloy#tabIndex=0"
# LMENASAAC_url =    "https://www.lme.com/Metals/Non-ferrous/NASAAC#tabIndex=0"