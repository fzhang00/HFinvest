# -*- coding: utf-8 -*-
"""
Created on Sat Mar 13 10:25:05 2021


https://www.quandl.com/data/FRED-Federal-Reserve-Economic-Data?page=64

@author: haoli
"""
fed_ProjectionDir = "./inflatonEstimation"
fed_H15Dir = "./H15"
fed_BalanceSheetDir = "./balanceSheet"
fed_H15Dir = "./FFRate_Vol_Proj"


fed_overnightRateDir = "./overnight rate"

RepoDir = "./Repo"


#-------------inflation projection------

 # implies what market participants expect inflation to be in the next 5 years, on average
#based on 10 year and 5 year nominal and inflation adjusted Treasury securities. 
inflatonRate_proj_ListCost = [["5Year And 5Year Forward Inflation Expectation Rate", "FRED/T5YIFR"], 
["5Year Breakeven Inflation Rate",  "FRED/T5YIE"],
["10Year Breakeven Inflation Rate", "FRED/T10YIE"],
["20Year Breakeven Inflation Rate", "FRED/T20YIEM"],
["30Year Breakeven Inflation Rate", "FRED/T30YIEM"]]


# ############# H.15
# https://www.federalreserve.gov/datadownload/Choose.aspx?rel=H15
# https://www.federalreserve.gov/datadownload/Choose.aspx?rel=H15

# trends in prices and wages, employment, consumer spending and income, business investments, 
#and foreign exchange markets
H15_ListConst = [["Primary Credit Rate", "FRED/DPCREDIT"], #Discount window primary credit
["Effective Federal Funds Rate", "FRED/DFF"], #Federal funds (effective)
["Bank Prime Loan Rate", "FRED/DPRIME"],

#--------------------1. Commercial Paper --------------
["1M AA Financial Commercial Paper Rate",   "FRED/DCPF1M"],
["2M AA Financial Commercial Paper Rate",   "FRED/DCPF2M"],
["3M AA Financial Commercial Paper Rate",   "FRED/DCPF3M"],
["1M AA Nonfinancial Commercial Paper Rate", "FRED/DCPN30"],
["2M AA Nonfinancial Commercial Paper Rate", "FRED/DCPN2M"],
["3M AA Nonfinancial Commercial Paper Rate", "FRED/DCPN3M"],

#--------------------2. Treasury bills (secondary market) --------------
# ["4Week Treasury Bill-Secondary Market Rate", "FRED/WTB4WK"], "FRED/WTB6MS"], "FRED/WTB1YR"],
["4Week Treasury Bill-Secondary Market Rate",   "FRED/DTB4WK"],
["3Month Treasury Bill-Secondary Market Rate",  "FRED/DTB3"],
["6Month Treasury Bill-Secondary Market Rate",  "FRED/DTB6"],
["1year Treasury Bill-Secondary Market Rate",   "FRED/DTB1YR"],

# ---3 Treasury constant maturities
# ["1Month Treasury Constant Maturity Rate",  "FRED/WGS1MO"],
# ["20Year Treasury Constant Maturity Rate",  "FRED/WGS20YR"],
["1Month Treasury Constant Maturity Rate", "FRED/DGS1MO"],
["3Month Treasury Constant Maturity Rate", "FRED/DGS3MO"],
["6Month Treasury Constant Maturity Rate", "FRED/DGS6MO"],
["1Year Treasury Constant Maturity Rate", "FRED/DGS1"],
["2Year Treasury Constant Maturity Rate", "FRED/DGS2"],
["3Year Treasury Constant Maturity Rate", "FRED/DGS3"],
["5Year Treasury Constant Maturity Rate", "FRED/DGS5"],
["7Year Treasury Constant Maturity Rate", "FRED/DGS7"],
["10Year Treasury Constant Maturity Rate", "FRED/DGS10"],
["20Year Treasury Constant Maturity Rate", "FRED/DGS20"],
["30Year Treasury Constant Maturity Rate", "FRED/DGS20"],
# ["5Year Treasury Inflation-Indexed Security-Constant Maturity", "FRED/WFII5"],
# ["10Year Treasury Inflation-Indexed Security-Constant Maturity", "FRED/WFII10"],
["5Year Treasury Inflation-Indexed Security-Constant Maturity", "FRED/DFII5"],
["7Year Treasury Inflation-Indexed Security-Constant Maturity", "FRED/DFII7"],
#Based on the unweighted average bid yields for all TIPS with remaining terms to maturity of more than 10 years.
["Treasury Inflation Indexed Long-Term Average Yield-10yr TIPS", "FRED/DLTIIT"], 
["10Year Treasury Inflation-Indexed Security-Constant Maturity", "FRED/DFII10"],
["20Year Treasury Inflation-Indexed Security-Constant Maturity", "FRED/DFII20"],
["30Year Treasury Inflation-Indexed Security-Constant Maturity", "FRED/DFII30"]]
# ["MarketYield on TreasurySecurities 1M constant maturity-quoted on investment dayly", "FED/RIFLGFCM01_N_B"],
# ["MarketYield on TreasurySecurities 3M constant maturity-quoted on investment dayly", "FED/RIFLGFCM03_N_B"],
# ["MarketYield on TreasurySecurities 6M constant maturity-quoted on investment dayly", "FED/RIFLGFCM06_N_B"],
# ["MarketYield on TreasurySecurities 1Y constant maturity-quoted on investment dayly",    "FED/RIFLGFCY01_N_B"],
# ["MarketYield on TreasurySecurities 5Y constant maturity-quoted on investment dayly",    "FED/RIFLGFCY05_N_B"],
# ["MarketYield on TreasurySecurities 10Y constant maturity-quoted on investment dayly",   "FED/RIFLGFCY10_N_B"],
# ["MarketYield on TreasurySecurities 20Y constant maturity-quoted on investment dayly",   "FED/RIFLGFCY20_N_B"],



#
FFRate_vol_proj_ListConst = [ ["Effective Federal Funds Rate", "FRED/EFFR"], #same as in H15
["Effective Federal Funds Vol", "FRED/EFFRVOL"],
["Federal Funds Target UpperLimit",  "FRED/DFEDTARU"],
["Federal Funds Target LowLimit",    "FRED/DFEDTARL"],


["Effective Federal Funds Rate 99thPercentile", "FRED/EFFR99"],
["Effective Federal Funds Rate 75thPercentile", "FRED/EFFR75"],
["Effective Federal Funds Rate 25thPercentile", "FRED/EFFR25"],
["Effective Federal Funds Rate 1stPercentile", "FRED/EFFR1"],
#https://fred.stlouisfed.org/graph/fredgraph.csv?id=FEDTARMD
["pFed Funds Rate High",     "FRED/FEDTARRH"],
["pFed Funds Rate Median",   "FRED/FEDTARMD"],
["pFed Funds Rate Midpint",  "FRED/FEDTARRM"],
["pFed Funds Rate Low",      "FRED/FEDTARRL"],
["pFed Funds Rate CentralTendencyLow",       "FRED/FEDTARCTL"],
["pFed Funds Rate CentralTendencyMidpint",   "FRED/FEDTARCTM"],
["pFed Funds Rate CentralTendencyHigh",      "FRED/FEDTARCTH"]]


#world map:  https://geofred.stlouisfed.org/map/?th=ylgn&cc=5&rc=false&im=fractile&sb&lng=-29.9&lat=35.7&zm=2&sl&sv&sti=219&rt=country&at=Not%20Seasonally%20Adjusted,%20Annual,%20Percent%20of%20GDP,%20no_period_desc&fq=Annual&dt=2019-01-01&am=Average&un=lin
#General Government Revenue for United States (USAGGRGDP)
#US - https://alfred.stlouisfed.org/series?seid=GGGDTAUSA188N&utm_source=series_page&utm_medium=related_content&utm_term=related_resources&utm_campaign=alfred
governmentDebt_ListCost = []
["ProjCHAGeneral government gross debt",    "FRED/GGGDTPCNA188N"],
["ProjCHAGeneral government net lendborrow","FRED/GGNLBPCNA188N"],

["USGeneral Government Gross Debt",     "FRED/USAGGXWDGGDP"],
["ProjUSGeneral government gross debt",    "FRED/GGGDTPUSA188N"],

["USGeneral government net lendborrow-past", "FRED/GGNLBAUSA188N"],
["USGeneral Government Net LendBorrow",     "FRED/USAGGXCNLGDP"],


["ProjUSGeneral government net LendBorrow", "FRED/GGNLBPUSA188N"],
["", ""],
["", ""],
["", ""] 


FED_balanceSheet_ListConst = [ 
["Central Bank Liquidity Swaps held by the Federal Reserve-Maturing within 15 days",    "FRED/SWP15"],
["Central Bank Liquidity Swaps held by the Federal Reserve-Maturing 16 to 90 days",     "FRED/SWP1690"],
["Central Bank Liquidity Swaps held by the Federal Reserve-All Maturities",             "FRED/SWPT"],
# ["", ""],
["USTreasury securities held by the Federal Reserve", "FRED/TREAST"],
["USTreasury securities held by the Federal Reserve-Maturing 16 to 90 days", "FRED/TREAS1590"],
["USTreasury securities held by the Federal Reserve-Maturing 1 to 5 years", "FRED/TREAS1T5"],
["USTreasury securities held by the Federal Reserve-Maturing 5 to 10 years", "FRED/TREAS5T10"],
["USTreasury securities held by the Federal Reserve-Maturing over 10 years", "FRED/TREAS10Y"],
# ["", ""],
["Assets: Securities Held Outright-Mortgage-Backed Securities", "FRED/WSHOMCB"],
["Mortgage-backed securities held by the Federal Reserve-Maturing 1 year to 5 years", "FRED/MBS1T5"],
["Mortgage-backed securities held by the Federal Reserve-Maturing 5 year to 10 years", "FRED/MBS5T10"],
["Mortgage-backed securities held by the Federal Reserve: Maturing over 10 years", "FRED/MBS10Y"],
# ["", ""],
#sum of "Term deposits held by depository institutions," "U.S. Treasury, general account," "U.S. Treasury, supplementary financing account," "foreign official accounts," "service-related deposits," and "other deposits."
["Factors Absorbing Reserve Funds-Deposits with Federal Reserve Banks Other Than Reserve Balances", "FRED/WOFDRBORBL"],
["Factors Absorbing Reserve Funds-Treasury Cash Holdings", "FRED/WOFDRBTHA"],
["Factors Supplying Reserve Balances-Reserve Bank Credit", "FRED/WOFSRBRBC"],
# ["", ""],
["Factors Supplying Reserve Balances-Total Factors Supplying Reserve Funds", "FRED/WTFSRFL"],
["Factors Supplying Reserve Balances-Treasury Currency Outstanding",    "FRED/WTCOL"],
["Factors Supplying Reserve Balances-Securities Held Outright-Treasury Securities", "FRED/WSHOTSA"],
["Factors Supplying Reserve Balances-Securities Held Outright-Treasury Notes and Bond InflationIndexed",    "FRED/WSHONBIIL"],
["Factors Supplying Reserve Balances-Securities Held Outright-Treasury Notes and Bond",                     "FRED/WSHONBNL"],
["Factors Supplying Reserve Balances-Securities Held Outright-Treasury Notes and Bond InflationCompensation", "FRED/WSHOICL"],

["Assets-Other Factors Supplying Reserve Balances-Other Federal Reserve assets_changePerWeeek avgWed", "FED/RESH4SO_XAW_XCH1_N_WW"],
# ["All Federal Reserve Banks: Total Assets", ""],
["All Federal Reserve Banks-Total Assets",                              "FRED/WALCL"],
["Liabilities-Total Liabilities Less Eliminations From Consolidation",  "FRED/WLTLECL"],
["Liabilities-Total Liabilities Eliminations From Consolidation",       "FRED/WLTEC"], #Millions of Dollars Not Seasonally Adjusted, These data are amounts that are eliminated when consolidating the balance sheets of the 12 Reserve Banks into a single balance sheet.
["Liabilities-Deposits Eliminations From Consolidation",                "FRED/WLDECL"],
["Liabilities-Federal Reserve Notes-Net of FR Bank Holdings",           "FRED/WLFN"],
["Liabilities: Other Liabilities and Accrued Dividends Plus Interest on Federal Reserve Notes Due to USTreasury", "FRED/WLAD"],

#This item indicates the value of securities lent to primary dealers. 
#The loans, which are fully collateralized by other U.S. Treasury securities, are awarded based on competitive bidding in a daily auction. 
#A minimum bid rate is imposed to limit borrowing to securities that are in high demand or "on special.
["Memorandum Item-Securities Lent to Dealers-Million",  "FRED/WSDEALL"],
["Memorandum item-Securities Lent to Dealers-Billion",  "FRED/WSDEAL"],
["Memorandum item-Securities Lent to Dealers-Overnight Facility", "FRED/WSDONT"]]



#--------------overnight short term interest rate------------------
overnightRate_ListCost =[ ["Interest Rate on Excess Reserves",    "FRED/IOER"],
["Interest Rate on Required Reserves",  "FRED/IORR"],
#https://fred.stlouisfed.org/graph/fredgraph.csv?id=RIFSPPFAAD07NB
["Overnight AA Financial Commercial Paper Interest Rate",   "FRED/RIFSPPFAAD01NB"],
["7Day AA Financial Commercial Paper Interest Rate",        "FRED/RIFSPPFAAD07NB"],


["Overnight Bank Funding Rate", "FRED/OBFR"],#https://fred.stlouisfed.org/series/OBFR
["Overnight Bank Funding Vol", "FRED/OBFRVOL"],

["Overnight Bank Funding Rate 99thPercentile", "FRED/OBFR99"],
["Overnight Bank Funding Rate 75thPercentile", "FRED/OBFR75"],
["Overnight Bank Funding Rate 25thPercentile", "FRED/OBFR25"],
["Overnight Bank Funding Rate 1stPercentile", "FRED/OBFR1"]]

#Reverse Repurchase Agreements: Total Securities Sold by the Federal Reserve in the Temporary Open Market
#Overnight Reverse Repurchase Agreements: Total Securities Sold by the Federal Reserve in the Temporary Open Market
#When the Fed wants to tighten the money supply — removing money from the cash flow — it sells the bonds to the commercial banks using a repo.

repo_ListCost = [["Rev Repo Total Securities Sold by FED",   "FRED/RRPTTLD"],
["Rev Repo T-Securities Sold by FED",       "FRED/RRPTSYD"],
["Rev Overnight Repo",                      "FRED/RRPONTTLD"],
["Rev Overnight Repo T-Securitie",          "FRED/RRPONTSYD"],

["Rev Bank Credit-Repo", "FRED/WREPO"],

#Term Repurchase Agreements: Total Securities Purchased by the Federal Reserve in the Temporary Temporary Open Market
["Term Repo Total Securities Purchased by FED", "FRED/RPTMTTLD"], 
["Term Repo MortgageBacked Securities Purchased by FED", "FRED/RPTMMBSD"],
["Term Repo Federal Agency Securities Purchased by FED", "FRED/RPTMAGYD"],
["Factors Supplying Reserve Balances-Repurchase Agreements", "FRED/WORAL"],

["Rev Repo held by FED-Maturing within 15 days", "FRED/RREP15"],
["Repo held by FED-Maturing within 15 days", "FRED/REP15"] ]
# ["", ""],
# ["", ""],
# ["", ""],
# ["", ""] 
#------------------------------








