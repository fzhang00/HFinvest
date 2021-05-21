# -*- coding: utf-8 -*-
"""
Created on Sat Mar 13 10:25:05 2021


https://www.quandl.com/data/FRED-Federal-Reserve-Economic-Data?page=64

https://www.federalreserve.gov/releases/z1/default.htm 
https://www.federalreserve.gov/releases/z1/20210311/html/default.htm


Main Economic Indicators
Sources > Organization for Economic Co-operation and 
https://fred.stlouisfed.org/release?rid=205


Quarterly: D.3 Debt Outstanding by Sector
 Households and Nonprofit Organizations; Consumer Credit; Liability, Level (HCCSDODNS)
 
 L.1 Credit Market Debt Outstanding
 
 National Accounts
 https://fred.stlouisfed.org/categories/32992
 Flow of Funds (35,000+)
 National Income & Product Accounts (13,000+)
Federal Government Debt (6+)
Flow of Funds (35,000+)
U.S. Trade & International Transactions (300+)



 General Government; Operating Surplus, Net, Flow
 Z.1 Financial Accounts of the United States
Quarterly: F.3 Distribution of National Income
Quarterly: F.105 General Government





G.17 Industrial Production and Capacity Utilization
Industrial Production and Capacity Utilization: Summary: Monthly, Seasonally Adjusted
Industrial Production Indexes: Market and Industry Group: Monthly, Seasonally Adjusted
 https://fred.stlouisfed.org/series/INDPRO/?utm_source=fred-glance-widget&utm_medium=widget&utm_campaign=fred-glance-widget
 
 
 Industrial Production and Capacity Utilization: Summary:
https://fred.stlouisfed.org/release/tables?rid=13&eid=49670#snid=49672


Industry Based
Categories > Prices > Producer Price Indexes (PPI)
https://fred.stlouisfed.org/categories/33584

     
Shopping lines: The evolution of retail in the U.S.
https://fredblog.stlouisfed.org/2015/12/shopping-lines-the-evolution-of-retail-in-the-u-s/


Total Business Inventories
https://fred.stlouisfed.org/tags/series?t=mtis



GDP_ListCost
unemployment_ListCost 
@author: haoli
"""

#-----------------------------------
GDP_ListCost = []

["Real GDP_Q","FRED/GDPC1"],
["World Real GDP_M",        "EIA/STEO_RGDPQ_WORLD_M"],
["Real GNPbyGDP_ROUTPUT",   "FRBP/ROUTPUT_MOSTRECENT"],

["Real Potential GDP",          "FRED/GDPPOT"],
["Nominal Potential GDP","FRED/NGDPPOT"],

["Growth Rate Real GDP_Median", "FRED/GDPC1MD"],

["", ""],
["", ""],
["", ""],
["", ""],
["", ""],
["", ""],

#--------------------------------------------


# ["NaturalRate Unemployment ShortTerm","FRED/NROUST"],
# the total number of people
unemploymentPeopleCount_ListCost = []
["All Employees-Total Nonfarm",         "FRED/PAYEMS"],
["Civilian Employment Level",           "FRED/CE16OV"],
["Unemployment Level",                  "FRED/UNEMPLOY"],

["Initial Claims-4W MA", "FRED/IC4WSA"], # number
["Initial Claims", "FRED/ICSA"],

# rate by Time
unemploymentByTime_ListCost = []
["Average Duration of Unemployment", "FRED/UEMPMEAN"],
["Of Total Unemployed-Percent Unemployed Less than 5 Weeks",    "FRED/LNS13008397"],
["Of Total Unemployed-Percent Unemployed 5 to 14 Weeks",        "FRED/LNS13025701"],
["Of Total Unemployed-Percent Unemployed 15 to 26 Weeks",       "FRED/LNS13025702"],
["Of Total Unemployed, Percent Unemployed 27 Weeks and over",   "FRED/LNS13025703"],

# rate
unemploymentByStructure_ListCost = []
["Civilian Unemployment Rate-noAdj",    "FRED/UNRATENSA"],
["3Civilian Unemployment Rate",            "FRED/UNRATE"],
["1Persons Unemployed 15 weeks or longer", "FRED/U1RATE"],
["2Unemployment Rate-Job Losers",          "FRED/U2RATE"],
["4Special Unemployment Rate-Unemployed and Discouraged Workers",          "FRED/U4RATE"],
["5Special Unemployment Rate-Unemployed and Marginally Attached Workers",  "FRED/U5RATE"],
["6Total unemployed-plus all marginally attached workers plus total employed part time for economic reasons ",          "FRED/U6RATE"],

["", ""],
["", ""],
["", ""],
["", ""],
["", ""],
["", ""],


#Fourth Quarter to Fourth Quarter Percent Change Not Seasonally Adjusted, Projections of personal consumption expenditures (PCE) inflation rate are fourth quarter growth rates, that is, percentage changes from the fourth quarter of the prior year to the fourth quarter of the indicated year.
#PCE (Personal Consumption Expenditures) inflation rate is the percentage rates of change in the price index for personal consumption expenditures (PCEPI)

#FOMC Summary of Economic Projections for the Personal Consumption Expenditures Inflation Rate, Range, High
["PersonalConsumptionExpenditures InflationRate High",      "FRED/PCECTPIRH"],
["PersonalConsumptionExpenditures InflationRate Median",    "FRED/PCECTPIMD"],
["PersonalConsumptionExpenditures InflationRate Midpoint",  "FRED/PCECTPIRM"],
["PersonalConsumptionExpenditures InflationRate Low",       "FRED/PCECTPIRL"],
["Longer Run PersonalConsumptionExpenditures InflationRate CentralTendencyHigh",    "FRED/PCECTPICTHLR"], 
["Longer Run PersonalConsumptionExpenditures InflationRate CentralTendencyMidpint", "FRED/PCECTPICTMLR"],
["Longer Run PersonalConsumptionExpenditures InflationRate CentralTendencyLow",     "FRED/PCECTPICTLLR"],
# https://www.quandl.com/data/FRED/JCXFECTM-FOMC-Summary-of-Economic-Projections-for-the-Personal-Consumption-Expenditures-less-Food-and-Energy-Inflation-Rate-Central-Tendency-Midpoint


["PCE less Food and Energy InflationRate High",     "FRED/JCXFERH"],
["PCE less Food and Energy InflationRate Midpoint", "FRED/JCXFERM"],
["PCE less Food and Energy InflationRate Median", "FRED/JCXFEMD"],
["PCE less Food and Energy InflationRate Low",    "FRED/JCXFERL"],

["PCE less Food and Energy InflationRate CentralTendencyHigh",      "FRED/JCXFECTH"],
["PCE less Food and Energy InflationRate CentralTendencyMidpoint",  "FRED/JCXFECTM"],
["PCE less Food and Energy InflationRate CentralTendencyLow",       "FRED/JCXFECTL"],
["", ""],
["", ""],
["", ""],
["", ""],
["", ""],
["", ""],
["USGeneral government net lendborrow","FRED/GGNLBPUSA188N"],
["CHAGeneral government net lendborrow","GGNLBPCNA188N"],
["CHAGeneral government gross debt","FRED/GGGDTPCNA188N"],
["",""],
["", ""],
["", ""],
["", ""],
["", ""],
["", ""],
["", ""],
["", ""],
["", ""],
["Economic Policy Uncertainty Index US", "FRED/USEPUINDXD"],
["Equity Market-related Economic Uncertainty Index", "FRED/WLEMUINDXD"],
["NBER based Recession Indicators-US from Peak through the Period preceding Trough", "FRED/USRECDP"],
["NBER based Recession Indicators-US from Peak through Trough", "FRED/USRECDM"],
["NBER based Recession Indicators-US from the Period following Peak through Trough", "FRED/USRECD"],
["", ""],
["", ""],
["", ""],
["", ""],
["", ""],

# Effective Federal Funds Rate and Overnight Bank Funding Rate
["", ""],
["", ""],
["", ""],
["", ""],
["", ""],

["", ""],
["", ""],
["", ""],
["", ""],
["", ""],
["", ""],
["", ""],
["", ""],


["", ""],
["", ""],
["", ""],
["", ""],
["", ""],




#------------------------







