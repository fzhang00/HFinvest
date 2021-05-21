# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 13:11:58 2021

@author: haoli
"""

import requests
import sp500Const as const

import pandas as pd  
import xlrd
# pip install xlrd
#import_file_path = filedialog.askopenfilename()

def downloadShPE_gurufocus(fillpath):
    f = open(fillpath, 'wb')  
    
    # url='https://www.lme.com/Metals/Non-ferrous#060d7ad1-4aa2-4dca-8999-accdb19e581f-tab-0'
    url='https://www.gurufocus.com/download_sector_shiller_pe.php'
    r = requests.get(url, allow_redirects=True)
    # open('test5.xls', 'wb').write(r.content)
    
    f.write(r.content)
    f.close()
    
    # df = r.json()
    # print (df)
# test = 'test.txt'   
downloadShPE_gurufocus(const.shillerPE_FillPath_const)
# downloadShPE_gurufocus(test)



# xl = pd.ExcelFile(const.shillerPE_FillPath_const)
# xl.head(5)

# wb = xlrd.open_workbook(const.shillerPE_FillPath_const, encoding_override='unicode')
# wb = xlrd.open_workbook(const.shillerPE_FillPath_const, encoding_override='unicode')

# df = pd.read_excel(const.shillerPE_FillPath_const,header=0)
# df = pd.read_excel(const.shillerPE_FillPath_const)


