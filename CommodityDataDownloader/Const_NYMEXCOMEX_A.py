# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 13:15:30 2021

http://www.kitconet.com/



https://www.lme.com/api/Lists/StockBreakdownReportPaging/Download?fileId=11714&fileName=Commitments%20of%20Traders%20Report%20-%20CA%20-%2023%20April%202021.xls

@author: haoli
"""

commodityDir = "./data"
commodityNYMEXCOMEXDir       = commodityDir + "/NYMEXCOMEX"
commodityNYMEXCOMEX_fileDir  = commodityNYMEXCOMEXDir  + "/temp" #"./data/LME/temp"

CME_deliveryReport_dir = commodityDir + '/CME_deliveryReport'
CME_positionOffsetReport_dir = CME_deliveryReport_dir + '/OI_shortLongPositionReport'
CME_gainStock_Tuesday_dir = CME_deliveryReport_dir + '/gain_Stock_weekly_Tuesday'
CME_bonds_dilivered_Q = CME_deliveryReport_dir + '/bondsDelivered_Q' 


comexWebsite_OI_shortLongPosition_List = [["OpentInterest_shortLongPosition_deliverable", 'https://www.cmegroup.com/delivery_reports/position-offset-report-deliverable-product.csv'],
                          ["OpentInterest_shortLongPosition_NonDeliverable", 'https://www.cmegroup.com/delivery_reports/position-offset-report-nondeliverable-product.csv'   ] ]

comexWebsite_gainStock_Tuesday_List = [['GainStock_weekly', 'https://www.cmegroup.com/delivery_reports/stocks-of-grain-updated-tuesday.xlsx']]

comexWebsite_bondsDelivered_Q_List = [['T_bondsDelivered', 'https://www.cmegroup.com/market-data/reports/CUSIPS-delivered-for-financial-contracts.xls']]

#--------daily volume and open interest--------------------------------
CME_daily_Vol_OI = './CME_daily_Vol_openInterest'
CME_Vol_openInterest_Agricultural   = CME_daily_Vol_OI + '/CME_Vol_openInterest_Agricultural'
CME_Vol_openInterest_Energy         = CME_daily_Vol_OI + '/CME_Vol_openInterest_Energy'
CME_Vol_openInterest_Equity         = CME_daily_Vol_OI + '/CME_Vol_openInterest_Equity'
CME_Vol_openInterest_FX             = CME_daily_Vol_OI + '/CME_Vol_openInterest_FX'
CME_Vol_openInterest_InterestRate   = CME_daily_Vol_OI + '/CME_Vol_openInterest_InterestRate'
CME_Vol_openInterest_Metal          = CME_daily_Vol_OI + '/CME_Vol_openInterest_Metal'

fileName_daily_Voi_Agricultural = 'daily_Voi_Agricultural'
fileName_daily_Voi_Energy       = 'daily_Voi_Energy'
fileName_daily_Voi_Equity       = 'daily_Voi_Equity'
fileName_daily_Voi_FX           = 'daily_Voi_FX'
fileName_daily_Voi_InterestRate = 'daily_Voi_InterestRate'
fileName_daily_Voi_Metal        = 'daily_Voi_Metal'

url_daily_Voi_Agricultural  = 'https://www.cmegroup.com/market-data/volume-open-interest/agriculture-commodities-volume.html'
url_daily_Voi_Energy        = 'https://www.cmegroup.com/market-data/volume-open-interest/energy-volume.html'
url_daily_Voi_Equity        = 'https://www.cmegroup.com/market-data/volume-open-interest/equity-volume.html'
url_daily_Voi_FX            = 'https://www.cmegroup.com/market-data/volume-open-interest/fx-volume.html'
url_daily_Voi_InterestRate  = 'https://www.cmegroup.com/market-data/volume-open-interest/interest-rate-volume.html'
url_daily_Voi_Metal         = 'https://www.cmegroup.com/market-data/volume-open-interest/metals-volume.html'

#----------stock------------------------------
goldKey         = "Gold_Stocks"
goldKiloKey     = "Gold_Kilo_Stocks"
silverKey       = "Silver_stocks"
cuKey           = "Copper_Stocks"
PAPLKey         = "PA-PL_Stck_Rprt"
alKey           = "Aluminum_Stocks"
znKey           = "Zinc_Stocks"
pbKey           = "Lead_Stocks" 

#https://www.cmegroup.com/clearing/operations-and-deliveries/registrar-reports.html
dict_COMEX_Stock_url = {
    goldKey         : "http://www.cmegroup.com/delivery_reports/Gold_Stocks.xls",
    goldKiloKey    : "http://www.cmegroup.com/delivery_reports/Gold_Kilo_Stocks.xls",
    silverKey       : "http://www.cmegroup.com/delivery_reports/Silver_stocks.xls",
    cuKey           : "http://www.cmegroup.com/delivery_reports/Copper_Stocks.xls",
    PAPLKey         : "http://www.cmegroup.com/delivery_reports/PA-PL_Stck_Rprt.xls",
    alKey           : "http://www.cmegroup.com/delivery_reports/Aluminum_Stocks.xls",
    znKey           : "http://www.cmegroup.com/delivery_reports/Zinc_Stocks.xls",
    pbKey           : "http://www.cmegroup.com/delivery_reports/Lead_Stocks.xls"
    }



GoldStocks      = "http://www.cmegroup.com/delivery_reports/Gold_Stocks.xls"
GoldKiloStocks  = "http://www.cmegroup.com/delivery_reports/Gold_Kilo_Stocks.xls"
SilverStocks    = "http://www.cmegroup.com/delivery_reports/Silver_stocks.xls"
CopperStocks    = "http://www.cmegroup.com/delivery_reports/Copper_Stocks.xls"
PlatinumandPalladiumStocks  = "http://www.cmegroup.com/delivery_reports/PA-PL_Stck_Rprt.xls"
AluminumStocks  = "http://www.cmegroup.com/delivery_reports/Aluminum_Stocks.xls"
ZincStocks      = "http://www.cmegroup.com/delivery_reports/Zinc_Stocks.xls"
LeadStocks      = "http://www.cmegroup.com/delivery_reports/Lead_Stocks.xls"


comexWebsite_StockList = [["Gold_Stocks", GoldStocks],
                            ["Gold_Kilo_Stocks", GoldKiloStocks],
                            ["Silver_stocks", SilverStocks],
                            ["Copper_Stocks", CopperStocks],
                            ["PA-PL_Stck_Rprt", PlatinumandPalladiumStocks],
                            ["Aluminum_Stocks", AluminumStocks],
                            ["Zinc_Stocks", ZincStocks],
                            ["Lead_Stocks", LeadStocks]]

# KeyWords = ["TOTAL REGISTERED", "TOTAL ELIGIBLE", "COMBINED TOTAL"]

