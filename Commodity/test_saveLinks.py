# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 10:25:17 2021

@author: haoli
"""


# URL = 'https://www.lme.com/Market-Data/Reports-and-data/Open-interest/MOI'






import time
from selenium import webdriver
  

def downloadExcelFile(targetDir, fileName, url):
    makeTodayDataDir(targetDir)    
    newFilefullPath = targetDir + '/' + fileName
    
    if os.path.isfile(newFilefullPath):
        os.remove(newFilefullPath)
        print('file removed: ' + newFilefullPath)
    
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3"}
    # reg_url = url
    req = Request(url = webAddress, headers = headers) 
    html = urlopen(req).read()  
    with open(newFilefullPath, 'wb') as outfile:
        outfile.write(html)   
    
    print('Downloaded weekly trader report: ' + newFilefullPath)  
  
def save_traderReport_weekly(url, targetDir):
    driver = webdriver.Chrome('../chromedriver.exe')
    driver.get(url)
    time.sleep(2)    
    
    elems = driver.find_elements_by_tag_name('a')
    
    
    for elem in elems:
        href = elem.get_attribute('href')
        str_Inhref = 'StockBreakdownReportPaging'
        str_InText = 'commitments of traders report'
        if str_InText in (elem.text).lower(): # if str_Inhref in href: # is not None:  
            d1 = (elem.text).split('(')
            d2 = d1[0].split('.')
            fileName = d2[0].strip() + '.xls'
            print (fileName)
    
    # print(str(count) +' : ' + href)
    print() 
# url = 'https://www.lme.com/Market-Data/Reports-and-data/Open-interest/MOI'

url = 'https://www.lme.com/en-GB/Market-Data/Reports-and-data/Commitments-of-traders/Copper'  
targetDir = ''
save_traderReport_weekly(url, targetDir)

# 1 : https://www.lme.com/api/Lists/StockBreakdownReportPaging/Download?fileId=11698&fileName=Market%20Open%20Interest%20-%2020%20April%202021.xls

# 2 : https://www.lme.com/api/Lists/StockBreakdownReportPaging/Download?fileId=11693&fileName=Market%20Open%20Interest%20-%2019%20April%202021.xls

# 3 : https://www.lme.com/api/Lists/StockBreakdownReportPaging/Download?fileId=11688&fileName=Market%20Open%20Interest%20-%2016%20April%202021.xls

# 4 : https://www.lme.com/api/Lists/StockBreakdownReportPaging/Download?fileId=11661&fileName=Market%20Open%20Interest%20-%2015%20April%202021.xls

# 5 : https://www.lme.com/api/Lists/StockBreakdownReportPaging/Download?fileId=11656&fileName=Market%20Open%20Interest%20-%2014%20April%202021.xls

# 6 : https://www.lme.com/api/Lists/StockBreakdownReportPaging/Download?fileId=11649&fileName=Market%20Open%20Interest%20-%2013%20April%202021.xls

# 7 : https://www.lme.com/api/Lists/StockBreakdownReportPaging/Download?fileId=11644&fileName=Market%20Open%20Interest%20-%2012%20April%202021.xls

# 8 : https://www.lme.com/api/Lists/StockBreakdownReportPaging/Download?fileId=11639&fileName=Market%20Open%20Interest%20-%2009%20April%202021.xls

# 9 : https://www.lme.com/api/Lists/StockBreakdownReportPaging/Download?fileId=11612&fileName=Market%20Open%20Interest%20-%2008%20April%202021.xls

# 10 : https://www.lme.com/api/Lists/StockBreakdownReportPaging/Download?fileId=11607&fileName=Market%20Open%20Interest%20-%2007%20April%202021.xls

# 11 : https://www.lme.com/api/Lists/StockBreakdownReportPaging/Download?fileId=11569&fileName=Market%20Open%20Interest%20Monthly%20-%20March%202021.xls

# 12 : https://www.lme.com/api/Lists/StockBreakdownReportPaging/Download?fileId=11359&fileName=Market%20Open%20Interest%20Monthly%20-%20February%202021.xls

# 13 : https://www.lme.com/api/Lists/StockBreakdownReportPaging/Download?fileId=11172&fileName=Market%20Open%20Interest%20Monthly%20-%20January%202021.xls

# 14 : https://www.lme.com/api/Lists/StockBreakdownReportPaging/Download?fileId=11027&fileName=Market%20Open%20Interest%20Monthly%20-%20December%202020.xls

# 15 : https://www.lme.com/api/Lists/StockBreakdownReportPaging/Download?fileId=10772&fileName=Market%20Open%20Interest%20Monthly%20-%20November%202020.xls

# 16 : https://www.lme.com/api/Lists/StockBreakdownReportPaging/Download?fileId=9481&fileName=Market%20Open%20Interest%20Monthly%20-%20October%202020.xls

# 17 : https://www.lme.com/api/Lists/StockBreakdownReportPaging/Download?fileId=9255&fileName=Market%20Open%20Interest%20Monthly%20-%20August%202020.xls

# 18 : https://www.lme.com/api/Lists/StockBreakdownReportPaging/Download?fileId=9152&fileName=Market%20Open%20Interest%20Monthly%20-%20July%202020.xls

# 19 : https://www.lme.com/api/Lists/StockBreakdownReportPaging/Download?fileId=9114&fileName=Market%20Open%20Interest%20Monthly%20-%20June%202020.xls

# 20 : https://www.lme.com/api/Lists/StockBreakdownReportPaging/Download?fileId=8920&fileName=Market%20Open%20Interest%20Monthly%20-%20May%202020.xls

