# -*- coding: utf-8 -*-
"""
Created on Fri May 14 10:32:38 2021

@author: haoli
"""
# import sys
# sys.path.append("../")
import os

# SP500_Ratios_Dir = "./SP500_Ratios"

# SP500_Ratios_dir_PE = './SP500_Ratios/PE' 

def makedir_ifnonexists(directory):
    if not os.path.exists(directory):
        os.mkdir(directory)

SP500_Ratios_dir_PE = './PE' 

SP500_Ratios_dir_ShillerPE = SP500_Ratios_dir_PE + '/ShillerPE'

makedir_ifnonexists(SP500_Ratios_dir_PE)
makedir_ifnonexists(SP500_Ratios_dir_ShillerPE)


# commodityLMEDir         = commodityDir + "/LME"      #"./data/LME"
# # commodityLME_workDir    = commodityLMEDir  + "/temp" #"./data/LME/temp"
# commodityLME_workDir_A    = commodityLMEDir  + "/temp_A" #"./data/LME/temp"



_Guru_shillerSector_URL = 'https://www.gurufocus.com/download_sector_shiller_pe.php'

_multpl_shillerTotal_URL = 'https://www.multpl.com/shiller-pe/table/by-month'

_Guru_sp500_PE_totalNormal_URL = 'https://www.gurufocus.com/economic_indicators/57/pe-ttm-of-sp-500-index'