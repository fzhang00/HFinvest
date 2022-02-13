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

Aluminium_url   = 'https://www.lme.com/en/Metals/Non-ferrous/LME-Aluminium#Trading+day+summary'#'https://www.lme.com/en/Metals/Non-ferrous/LME-Aluminium'           
Copper_url      = 'https://www.lme.com/en/Metals/Non-ferrous/LME-Copper#Trading+day+summary'#'https://www.lme.com/en/Metals/Non-ferrous/LME-Copper'              
Zinc_url        = 'https://www.lme.com/en/Metals/Non-ferrous/LME-Zinc#Trading+day+summary'#'https://www.lme.com/en/Metals/Non-ferrous/LME-Zinc'                
Nickel_url      = 'https://www.lme.com/en/Metals/Non-ferrous/LME-Nickel#Trading+day+summary'#'https://www.lme.com/en/Metals/Non-ferrous/LME-Nickel'              
Lead_url        = 'https://www.lme.com/en/Metals/Non-ferrous/LME-Lead#Trading+day+summary'#'https://www.lme.com/en/Metals/Non-ferrous/LME-Lead' 
Tin_url         = 'https://www.lme.com/en/Metals/Non-ferrous/LME-Tin#Trading+day+summary'#'https://www.lme.com/en/Metals/Non-ferrous/LME-Tin'                 
AluminiumAlloy_url  = 'https://www.lme.com/en/Metals/Non-ferrous/LME-Aluminium-Alloy#Trading+day+summary'#'https://www.lme.com/en/Metals/Non-ferrous/LME-Aluminium-Alloy'                  
NASAAC_url      = 'https://www.lme.com/en/Metals/Non-ferrous/LME-NASAAC#Trading+day+summary'#'https://www.lme.com/en/Metals/Non-ferrous/LME-NASAAC'              

Cobalt_url      = 'https://www.lme.com/en/Metals/EV/LME-Cobalt#Trading+day+summary'#'https://www.lme.com/en/Metals/EV/LME-Cobalt'
Lithium_url     = 'https://www.lme.com/en/Metals/EV/About-Lithium' #'https://www.lme.com/en/Metals/EV/Lithium-prices'

# SteelRebar_url  = 'https://www.lme.com/en/Metals/Ferrous/LME-Steel-Rebar'
SteelRebar_url  = 'https://www.lme.com/en/Metals/Ferrous/lme-Steel-Rebar-FOB-Turkey-Platts#Trading+day+summary'
#Gold_url    = 'https://www.lme.com/en/Metals/Precious/LME-Gold'
Gold_url    = 'https://www.lme.com/en/Metals/Precious/LME-Gold#Trading+day+summary'
# Silver_url  = 'https://www.lme.com/en/Metals/Precious/LME-Silver'
Silver_url  = 'https://www.lme.com/en/Metals/Precious/LME-Silver#Trading+day+summary'    
Key_Aluminium       = 'Aluminium'        
Key_Copper          = 'Copper'  
Key_Zinc            = 'Zinc'  
Key_Nickel          = 'Nickel'    
Key_Lead            = 'Lead'               
Key_Tin             = 'Tin' 
Key_AluminiumAlloy  = 'Aluminium Alloy'             
Key_NASAAC          = 'NASAAC' 
              
Key_Cobalt      = 'Cobalt'
Key_Lithium     = 'Lithium'
Key_SteelRebar  = 'Steel Rebar'
KEY_Gold = 'Gold' 
KEY_Silver = 'Silver'  

DICT_URL_A  = { 
                Key_Aluminium       : Aluminium_url,   
                Key_Copper          : Copper_url  ,  
                Key_Zinc            : Zinc_url      ,
                Key_Nickel          : Nickel_url    ,
                Key_Lead            : Lead_url      ,    
                Key_Tin             : Tin_url       ,
                Key_AluminiumAlloy  : AluminiumAlloy_url ,            
                Key_NASAAC          : NASAAC_url ,
                Key_Cobalt			: Cobalt_url    ,
                # Key_Lithium			: Lithium_url   ,
                Key_SteelRebar		: SteelRebar_url,
                KEY_Gold			: Gold_url     ,
                KEY_Silver			: Silver_url     }


# DICT_URL_A_FILENAME = { KEY_NONFERROUS : _NONFERROUS_FILENAME,  KEY_GOLD : _GOLD_FILENAME, KEY_SILVER : _SILVER_FILENAME }



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

