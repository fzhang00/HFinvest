# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 11:43:57 2021

@author: haoli
"""

import sys
sys.path.append("../")
import const_common as constA
import downloadUpdateData as myData1

# import Const_corpBond as const

_ON_Reverse_Rep = 'RRPONTSYD'
_path_ON_Reverse_Rep = './data/ON_Reverse_Rep.csv'

_ON_Rep = 'RPONTSYD'
_path_ON_Rep = './data/ON_Rep.csv'

_EffectiveRate = 'FEDFUNDS'
_path_EffectiveRate = './data/FederalFunds_EffectiveRate.csv'

def ON_Reverse_Rep():
    data_source = "fred"
    start_date = '1995-01-01' 
    end_date = constA.todayDate_str 
    api_key = None
    
    ticker = _ON_Reverse_Rep
    targetFillFullpath = _path_ON_Reverse_Rep    
    # myData1.download_update_Data_toPath(ticker, data_source, start_date, end_date, api_key, targetFillFullpath)

    ticker = _ON_Rep
    targetFillFullpath = _path_ON_Rep    
    myData1.download_update_Data_toPath(ticker, data_source, start_date, end_date, api_key, targetFillFullpath)


ON_Reverse_Rep()







# def downloadUpdate_corpBondRates():
#     fillNameTicker_List = const.corpBond_quandlList
#     targetDir = const.corpBondDir 
    
#     data_source = constA.quandlDataSource_const
#     start_date = '1995-01-01' 
#     end_date = constA.todayDate_str 
#     api_key = constA.quandlKey_const  
    
#     myData1.download_update_Data_byTicker_FillName_List(fillNameTicker_List, targetDir, 
#                                                         data_source, start_date, end_date, 
#                                                         api_key)



# downloadUpdate_corpBondRates()

# def combine_corpBondRates():
#     isCopyCol = False
#     sourceFillDir = const.corpBondDir
    
#     targetFillPath = "Corperation Bond Rates.csv"
    
#     df = myData1.combineFill_byDir(sourceFillDir, targetFillPath, isCopyCol)
#     # df = combineFill_byDir(sourceFillDir, isCopyCol) 
#     # df.index.name = 'Date'
#     df.to_csv(targetFillPath, float_format='%.3f')
    
# combine_corpBondRates()