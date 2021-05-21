# -*- coding: utf-8 -*-
"""
Created on Sat Mar 13 10:25:05 2021

https://www.quandl.com/data/FRED-Federal-Reserve-Economic-Data?page=64

@author: haoli
"""

#--------------------------------------------

"""
#Initial unemployment claims is a much-watched indicator of the economy. 
#It counts how many people have become eligible for unemployment insurance compensation in a particular week. 
#The data are available quickly and at a high frequency (weekly), but the series has the disadvantage of being highly volatile. 
#This is why FRED also offers a four-week moving average, shown in the graph above: Simply, it’s the average of the past four weeks. 
#Included in the graph is also a red line that indicates the lowest value of this statistic in the course of its history—in May 1969. 
#Currently, claims are around 230,000 per week; and, while this is low, it was lower for 126 weeks early in the sample period

"""
# ["NaturalRate Unemployment ShortTerm","FRED/NROUST"],
# the total number of people
unemploymentPeopleCount_InitialClaim_ListCost = [["All Employees-Total Nonfarm",         "FRED/PAYEMS"],
["Civilian Employment Level",   "FRED/CE16OV"],
["Unemployment Level",          "FRED/UNEMPLOY"],
["Initial Claims",          "FRED/ICSA"],
["Initial Claims-4W MA",    "FRED/IC4WSA"]] 


# rate by unemploymentDuration
unemploymentDuration_ListCost = [["Average Duration of Unemployment", "FRED/UEMPMEAN"],
["Of Total Unemployed-Percent Unemployed Less than 5 Weeks",    "FRED/LNS13008397"],
["Of Total Unemployed-Percent Unemployed 5 to 14 Weeks",        "FRED/LNS13025701"],
["Of Total Unemployed-Percent Unemployed 15 to 26 Weeks",       "FRED/LNS13025702"],
["Of Total Unemployed, Percent Unemployed 27 Weeks and over",   "FRED/LNS13025703"]]

"""
# unemployment u1, 2,3,4,5 https://www.stlouisfed.org/open-vault/2018/june/unemployment-number-to-watch
"""
unemployment_Alt_Measure_ListCost = [["Civilian Unemployment Rate-noAdj",        "FRED/UNRATENSA"],
["3Civilian Unemployment Rate",             "FRED/UNRATE"],
["1Persons Unemployed 15 weeks or longer",  "FRED/U1RATE"],
["2Unemployment Rate-Job Losers",           "FRED/U2RATE"],
["4Special Unemployment Rate-Unemployed and Discouraged Workers",          "FRED/U4RATE"],
["5Special Unemployment Rate-Unemployed and Marginally Attached Workers",  "FRED/U5RATE"],
["6Total unemployed-plus all marginally attached workers plus total employed part time for economic reasons ", "FRED/U6RATE"]]
