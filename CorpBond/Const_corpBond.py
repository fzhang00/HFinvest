# -*- coding: utf-8 -*-
"""
Created on Sat Mar 13 10:25:05 2021
http://www.cbonds.info/cis/eng/index/index_detail/group_id/153/

@author: haoli
"""

# "US Corporate Bonds Total Return Index",    "ML/TRI"
# "US AAA Corporate Bond Total Return Index", "ML/AAATRI"
# "US Corporate Bond A Total Return Index",   "ML/ATRI"
# "US Corporate BBB Total Return Index",      "ML/BBBTRI"
# "US B Corporate Bond Total Return Index",   "ML/BTRI"
# "Europe/Middle East/Africa (EMEA) Corporate Bond Total Return Index", "ML/EMHG"
# "IG Emerging Markets Corporate Bond Total Return Index", "ML/IGEM"

# "US AA Bond Index Yield",                   "ML/AAY"

# "US High Yield Corporate Bond Index_Yield", "ML/USTRI"
# "US High Yield BB Corporate Bond Index Yield", "ML/BBY"
# "US CCC-rated Bond Index Yield",            "ML/CCCY"

# "Emerging Markets High Grade Corporate Bond Index Yield", "ML/EMHGY"
# "Euro Emerging Markets Corporate Bond Index_Yield", "ML/EEMCBI"

# "US AA-rated Bond Index OAS",               "ML/AAOAS"
# "US B-rated Bond Index OAS",                "ML/BOAS"
# "US High Yield Corporate Bond Index OAS",   "ML/HYOAS"
# "Emerging Markets Corporate Bond Index OAS","ML/EMCBI"


corpBondDir = "./data"
#------------------------
corpBond_quandlList = [["US Corporate Bonds Total Return Index",    "ML/TRI"],
["US AAA Corporate Bond Total Return Index", "ML/AAATRI"],
["US Corporate Bond A Total Return Index",   "ML/ATRI"],
["US Corporate BBB Total Return Index",      "ML/BBBTRI"],
["US B Corporate Bond Total Return Index",   "ML/BTRI"],
["EuropeMiddleEastAfrica Corporate Bond Total Return Index", "ML/EMHG"],
["IG Emerging Markets Corporate Bond Total Return Index", "ML/IGEM"],

["US AA Bond Index Yield",                   "ML/AAY"],

["US High Yield Corporate Bond Index_Yield", "ML/USTRI"],
["US High Yield BB Corporate Bond Index Yield", "ML/BBY"],
["US CCC rated Bond Index Yield",            "ML/CCCY"],

["Emerging Markets High Grade Corporate Bond Index Yield", "ML/EMHGY"],
["Euro Emerging Markets Corporate Bond Index_Yield", "ML/EEMCBI"],

["US AA rated Bond Index OAS",               "ML/AAOAS"],
["US B rated Bond Index OAS",                "ML/BOAS"],
["US High Yield Corporate Bond Index OAS",   "ML/HYOAS"],
["Emerging Markets Corporate Bond Index OAS","ML/EMCBI" ]]
#------------------------Treasury Real Yield Curve Rates
corpBondNameList = ["US Corporate Bonds Total Return Index",
                "US AAA Corporate Bond Total Return Index", 
                "US Corporate Bond A Total Return Index",   
                "US Corporate BBB Total Return Index",      
                "US B Corporate Bond Total Return Index",   
                "Europe/Middle East/Africa (EMEA) Corporate Bond Total Return Index", 
                "IG Emerging Markets Corporate Bond Total Return Index", 
                
                "US AA Bond Index Yield",                  
                
                "US High Yield Corporate Bond Index_Yield", 
                "US High Yield BB Corporate Bond Index Yield", 
                "US CCC-rated Bond Index Yield",            
                
                "Emerging Markets High Grade Corporate Bond Index Yield", 
                "Euro Emerging Markets Corporate Bond Index_Yield", 
                
                "US AA-rated Bond Index OAS",               
                "US B-rated Bond Index OAS",                
                "US High Yield Corporate Bond Index OAS",   
                "Emerging Markets Corporate Bond Index OAS"]
