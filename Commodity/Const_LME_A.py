# -*- coding: utf-8 -*-
"""
@author: haoli
"""

commodityDir = "./data"
commodityLMEDir         = commodityDir + "/LME"      #"./data/LME"
# commodityLME_workDir    = commodityLMEDir  + "/temp" #"./data/LME/temp"
commodityLME_workDir_A    = commodityLMEDir  + "/temp_A" #"./data/LME/temp"

# KEY_NONFERROUS = 'NONFERROUS' 
# KEY_GOLD = 'Gold' 
# KEY_SILVER = 'Silver'  

# _NONFERROUS_FILENAME = 'nonFerrous_price_stock.csv'
# _GOLD_FILENAME = "gold_price_vol_OI.csv"
# _SILVER_FILENAME = "silver_price_vol_OI.csv"

# _NONFERROUS_PRICE_STOCK_URL = 'https://www.lme.com/Metals/Non-ferrous'
# _GOLD_PRICE_VOL_OI_URL     = "https://www.lme.com/Metals/Precious-metals/LME-Gold"
# _SILVER_PRICE_VOL_OI_URL   = "https://www.lme.com/Metals/Precious-metals/LME-Silver"


# DICT_URL_A = {KEY_NONFERROUS : _NONFERROUS_PRICE_STOCK_URL, KEY_GOLD : _GOLD_PRICE_VOL_OI_URL, KEY_SILVER  : _SILVER_PRICE_VOL_OI_URL }
# DICT_URL_A_FILENAME = { KEY_NONFERROUS : _NONFERROUS_FILENAME,  KEY_GOLD : _GOLD_FILENAME, KEY_SILVER : _SILVER_FILENAME }

#-------daily volume-----------------------
commodityLME_dailyVolumeDir     = commodityDir  + "/LME_Volume_Daily" 
#dialyVolume_url      = 'https://www.lme.com/LME-Clear/Technology/Reports/Volumes'
dialyVolume_url      = 'https://www.lme.com/en/Market-data/Reports-and-data/Volumes/Daily-volumes'

#---------------- weekly trader report----------

commodityLME_trderReportDir  = commodityDir + "/LME_TraderReport" 
trderReport_ALDir = commodityLME_trderReportDir +'/Aluminium'
trderReport_CADir = commodityLME_trderReportDir +'/Copper'
trderReport_goldDir = commodityLME_trderReportDir +'/Gold'
trderReport_silverDir = commodityLME_trderReportDir +'/Silver'

#https://www.lme.com/Market-Data/Reports-and-data/Commitments-of-traders#tabIndex=0
ALTraderReport_url      = 'https://www.lme.com/en/Market-data/Reports-and-data/Commitments-of-traders/Aluminium'
CATraderReport_url      = 'https://www.lme.com/en/Market-Data/Reports-and-data/Commitments-of-traders/Copper'
goldTraderReport_url    = 'https://www.lme.com/en/Market-data/Reports-and-data/Commitments-of-traders/LME-Gold'
silverTraderReport_url  = 'https://www.lme.com/en/Market-data/Reports-and-data/Commitments-of-traders/LME-Silver'

trderReport_Steel_rebarDir = commodityLME_trderReportDir +'/Steel_rebar'
Steel_rebarTraderReport_url  = 'https://www.lme.com/en/Market-data/Reports-and-data/Commitments-of-traders/LME-Steel-Rebar'

trderReport_NickelDir = commodityLME_trderReportDir +'/Nickel'
NickelTraderReport_url  = 'https://www.lme.com/en/Market-data/Reports-and-data/Commitments-of-traders/LME-Nickel'

trderReport_TinDir = commodityLME_trderReportDir +'/Tin'
TinTraderReport_url     = 'https://www.lme.com/en/Market-data/Reports-and-data/Commitments-of-traders/LME-Tin'

trderReport_ZincDir = commodityLME_trderReportDir +'/Zinc'
ZincTraderReport_url    = 'https://www.lme.com/en/Market-data/Reports-and-data/Commitments-of-traders/LME-Zinc'

trderReport_LeadDir = commodityLME_trderReportDir +'/Lead'
LeadTraderReport_url    = 'https://www.lme.com/en/Market-data/Reports-and-data/Commitments-of-traders/LME-Lead'


#-------daily Open interest-----------------------
commodityLME_openInterestDir    = commodityDir  + "/LME_OpenInterest" 

commodityLME_openInterestDir_base = commodityLME_openInterestDir + '/base_E' 
dialyOpenInterest_base_url      = 'https://www.lme.com/en/Market-data/Reports-and-data/Open-interest/Exchange-open-interest'

commodityLME_openInterestDir_precious = commodityLME_openInterestDir + '/precious_E'  
# dialyOpenInterest_precious_url  = 'https://www.lme.com/Market-Data/Reports-and-data/Open-interest/EOI#tabIndex=1'

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



           
     

