# -*- coding: utf-8 -*-
"""
Created on Wed May 19 10:41:41 2021

@author: haoli
"""

# import requests



import os
import time
from selenium import webdriver
def download_xlsFiles_CME(url, downloadDir):
    prefs = {"download.default_directory" : downloadDir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing_for_trusted_sources_enabled": False,
            "safebrowsing.enabled": False,            
            'download.manager.showWhenStarting': False,
            'helperApps.neverAsk.saveToDisk': 'text/csv/xls, application/vnd.ms-excel, application/octet-stream'
             }  #("network.http.response.timeout", 30) 
    
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome('chromedriver.exe', chrome_options = chromeOptions)  # Optional argument, if not specified will search path.
    time.sleep(1)
    driver.get(url)
    time.sleep(1)
    driver.quit()
    time.sleep(1)       
url = "http://www.cmegroup.com/delivery_reports/Gold_Stocks.xls"
downloadDir = 'G:\\test.xls'
download_xlsFiles_CME(url, downloadDir)


profile.set_preference('browser.download.manager.showWhenStarting', False)
# profile.set_preference('browser.download.dir', os.getcwd())
profile.set_preference('browser.download.dir', filePath)
profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv/xls')




# # http://kb.mozillazine.org/About:config_entries
# profile = webdriver.FirefoxProfile()

# # profile.set
# profile.set_preference('browser.download.folderList', 2)
# profile.set_preference('browser.download.manager.showWhenStarting', False)
# # profile.set_preference('browser.download.dir', os.getcwd())
# profile.set_preference('browser.download.dir', filePath)
# profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv/xls')

# driver = webdriver.Firefox('./geckodriver.exe', profile)
# # driver = webdriver.Chrome('chromedriver.exe',options = profile)  # Optional argument, if not specified will search path.

# # webdriver driver = new FirefoxDriver(profile)
# driver.navigate().to(url);


# #--------------------------

# from selenium import webdriver
# from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

# profile = webdriver.FirefoxProfile()
# profile.set_preference('browser.download.folderList', 2)
# profile.set_preference('browser.download.manager.showWhenStarting', False)
# profile.set_preference('browser.download.dir', os.getcwd())
# profile.set_preference('browser.helperApps.neverAsk.saveToDisk', ('application/vnd.ms-excel'))
# profile.set_preference('general.warnOnAboutConfig', False)
# profile.update_preferences()
# gecko_path = './geckodriver.exe'  #"path_to_geckodriver\\geckodriver.exe"
# path = "path_to_firefoxs\\Mozilla Firefox\\firefox.exe"
# binary = FirefoxBinary(path)
# driver = webdriver.Firefox(firefox_profile=profile,executable_path=gecko_path)



# #--------------------------



# # options = webdriver.ChromeOptions()  
# # # options.add_argument("--browser.download.folderList=2")
# # # options.add_argument("--browser.helperApps.neverAsk.saveToDisk = text/csv/xls")
# # # options.add_argument("--browser.download.di = L:/test.xls")
# # options.add_experimental_option('browser.download.folderList', 2)
# # options.add_experimental_option('browser.helperApps.neverAsk.saveToDisk', 'text/csv/xls')
# # options.add_experimental_option('browser.download.dir', filePath)

# # driver = webdriver.Chrome('chromedriver.exe', options = options)
# # driver.get(url)


# # driver = webdriver.Chrome('chromedriver.exe')  # Optional argument, if not specified will search path.
# # driver.get(url)
# #refresh the webpage first




# # # # url = 'https://www.python.org/static/img/python-logo@2x.png'

# # # myfile = requests.get(url)

# # # open('L:/test.xls', 'wb').write(myfile.content)


# # import wget

# # # url = "https://www.python.org/static/img/python-logo@2x.png"

# # # wget.download(url, 'L:/test.xls')

# # import requests

# # # url = 'https://readthedocs.org/projects/python-guide/downloads/pdf/latest/'

# # myfile = requests.get(url, allow_redirects=True)

# # open(filePath, 'wb').write(myfile.content)


# # import urllib
# # # dls = "http://www.muellerindustries.com/uploads/pdf/UW SPD0114.xls"
# # urllib.request.urlretrieve(url, filePath)  # For Python 3


