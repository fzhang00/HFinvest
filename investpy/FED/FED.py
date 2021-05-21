# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 11:43:57 2021

@author: haoli
"""

import sys
sys.path.append("../")
import const_common as constA
import downloadUpdateData as myData1

import Const_corpBond as const



def downloadUpdate_corpBondRates():
    fillNameTicker_List = const.corpBond_quandlList
    targetDir = const.corpBondDir 
    
    data_source = constA.quandlDataSource_const
    start_date = '1995-01-01' 
    end_date = constA.todayDate_str 
    api_key = constA.QUANDL_KEY  
    
    myData1.download_update_Data_byTicker_FillName_List(fillNameTicker_List, targetDir, 
                                                        data_source, start_date, end_date, 
                                                        api_key)

# downloadUpdate_corpBondRates()

def combine_corpBondRates():
    isCopyCol = False
    sourceFillDir = const.corpBondDir
    
    targetFillPath = "Corperation Bond Rates.csv"
    
    df = myData1.combineFill_byDir(sourceFillDir, targetFillPath, isCopyCol)
    # df = combineFill_byDir(sourceFillDir, isCopyCol) 
    # df.index.name = 'Date'
    df.to_csv(targetFillPath, float_format='%.3f')
    
# combine_corpBondRates()

