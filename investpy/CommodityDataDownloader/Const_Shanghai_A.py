# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 13:15:30 2021

http://www.kitconet.com/


@author: haoli
"""

commodityDir = "./data"
commodityShanghaiDir       = commodityDir + "/Shanghai"      #"./data/LME"
commodityShanghai_dataDir  = commodityShanghaiDir   + "/temp" #"./data/LME/temp"

commodityShanghaiDir_OIVolPrice = commodityDir + '/ShanghaitempOpenInterestVolumePrice'
commodityShanghai_dataDir_OIVolPrice  = commodityShanghaiDir_OIVolPrice + '/temp'

# SHStock_url_weekly = "http://www.shfe.com.cn/statements/dataview.html?paramid=weeklystock"

SHStock_url_weekly = 'http://www.shfe.com.cn/en/MarketData/dataview.html?paramid=week'
SHStockfileName_weekly = "ShanghaiStock_weekly.csv"
SH_openInterest_Vol_fileName_weekly = "Shanghai_OpenInterest_Volumn_weekly.csv"


#----not used
SHCopper_url_daily = 'http://www.shfe.com.cn/statements/dataview.html?paramid=delaymarket_cu'
SHCOPPERfileName = "SH_copper.csv"

SHcrudeOil_url_daily = 'http://www.shfe.com.cn/statements/dataview.html?paramid=delaymarket_sc'
SHcrudeOilfileName = "SH_crudeOil.csv"

SHgold_url_daily = 'http://www.shfe.com.cn/statements/dataview.html?paramid=delaymarket_cu'
SHCOPPERfileName = "SH_copper.csv"
#not used end


cuKey = 'CuFileName' 
cuBCKey = 'CuBCFileName'
alKey= 'ALFileName' 
znKey = 'ZnFileName' 
niKey = 'NiFileName' 
pbKey = 'LeadFileName' 
tinKey = 'TinFileName' 
goldKey = 'GoldFileName' 
silverKey = 'SilverFileName'  
 
SH_stockFileName_disct = {
    cuKey   : "SH_copperStock.csv",
    cuBCKey : "SH_copperBCStock.csv",
    alKey   : "SH_ALStock.csv",
    znKey   : "SH_zincStock.csv",
    niKey   : "SH_nickelStock.csv",
    pbKey   : "SH_leadStock.csv",
    tinKey  : "SH_tinStock.csv",
    goldKey : "SH_goldStock.csv", 
    silverKey : "SH_silverStock.csv"    
    }
SHFE_StockCol1 = 'On Warrant'
SHFE_StockCol2 = 'Deliverable'

SH_openInterestVolumn_FileName_disct = {
    cuKey   : "SH_copperOpenInterestVolume.csv",
    cuBCKey : "SH_copperBCOpenInterestVolume.csv",
    alKey   : "SH_ALOpenInterestVolume.csv",
    znKey   : "SH_zincOpenInterestVolume.csv",
    niKey   : "SH_nickelOpenInterestVolume.csv",
    pbKey   : "SH_leadOpenInterestVolume.csv",
    tinKey  : "SH_tinOpenInterestVolume.csv",
    goldKey : "SH_goldOpenInterestVolume.csv",
    silverKey : "SH_silverOpenInterestVolume.csv",  
    }

# SH_openInterestVolumn_FileName_disct = {
#     cuKey   : "SH_copperOpenInterestVolunm.csv",
#     cuBCKey : "SH_copperBCOpenInterestVolunm.csv",
#     alKey   : "SH_ALOpenInterestVolunm.csv",
#     znKey   : "SH_zincOpenInterestVolunm.csv",
#     niKey   : "SH_nickelOpenInterestVolunm.csv",
#     pbKey   : "SH_leadOpenInterestVolunm.csv",
#     tinKey  : "SH_tinOpenInterestVolunm.csv",
#     goldKey : "SH_goldOpenInterestVolunm.csv",
#     silverKey : "SH_silverOpenInterestVolunm.csv",   
#     }
SHFE_OIVolCol1 = 'OpenInterest'
# SHFE_OIVolCol2 = 'Volumn'
SHFE_OIVolCol2 = 'Volume'
SHFE_OIVolCol3 = 'TurnOver' #total money exchanged


# SH_stockFileName_disct = {
#     'CuFileName' : "SH_copperStock.csv",
#     'ALFileName' : "SH_ALStock.csv",
#     'ZnFileName' : "SH_zincStock.csv",
#     'NiFileName' : "SH_nickelStock.csv",
#     'LeadFileName' : "SH_leadStock.csv",
#     'TinFileName' : "SH_tinStock.csv",
#     'GoldFileName' : "LME_goldStock.csv", 
#     'SilverFileName' : "LME_silverStock.csv"    
#     }



#Deliverable = 4  On Warrant = 5 Stock = 4-5, 
#注册了仓单的货物就是期货库存，没有注册仓单的 就是现货库存








