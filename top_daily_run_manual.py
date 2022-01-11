"""
Top level python launcher

User must define a few constant: 

_PYTHON : the complete path to your Python exe
_ROOT_DIR: the complete path to the location of this repository
"""

from datetime import datetime
import os
# import key as pconst
import top_runner_util as util

_ROOT_DIR = os.getcwd() #pconst.ROOT_DIR
print(_ROOT_DIR)
today = datetime.today()


# ------------ Main Script ----------------------
print("Data downloader launcher")
os.chdir(_ROOT_DIR)

# ----------- List your script here----------------

"""
Examples: 

- To run a script on every business day, use run_daily(subfolder_name, script_name, timezone_name). 
    - New York timezone is "US/Eastern". London timezone is "GMT"
    - Example: run_daily("\\Commodity\\", "comodityDailyRun_A.py", "US/Eastern")
- To run a script on specific day of a week on weekly basis, use run_day_of_week(subfolder_name, script_name, day_of_week)
    - day_of_week: a integer. 0 is Monday, 6 is Sunday
    - Example: run_day_of_week("\\market_breadth\\", "run.py", 5)
- To run a script regardless of schedule, use run_script(subfolder_name, script_name)
    - Example: run_script("\\Commodity\\", "run.py")
"""



    #----Saturday --------
# util.run_script("\\Commodity\\", "SHFE_A.py")
# util.run_script("\\Commodity\\", "LME_weekly_traderReport.py")
# util.run_script("\\Commodity\\", "LME_A2.py")

    #----Tuesday --------
# util.run_script("\\Commodity\\", "COMEX_A_gainStock_Tuesday_weekly_Run.py") 

    #----weekday--------
# util.run_script("\\Commodity\\", "LME_A2.py")
# util.run_script("\\Commodity\\", "LME_daily_volume.py")    
# util.run_script("\\Commodity\\", "LME_daily_openInterest_E.py") 

# util.run_script("\\SP500_Ratios\\", "Guru_shiller_sectors.py")    
# util.run_script("\\Commodity\\", "COMEX_A.py")      
# util.run_script("\\Commodity\\", "COMEX_daily_openInterest_VOL.py")

    # -----FINRA---3ndWeekOfMonth--------
  
# util.run_script("\\FINRA\\", "FINRA_Margin_Statistics_3ndWeekOfMonth.py")


# util.run_script("\\Commodity\\", "LME_daily_openInterest_E.py")
# util.run_script("\\Fear_Greed\\", "Fear_Greed_CNN.py")

# util.run_script("\\Commodity\\", "LME_daily_volume.py") 
# util.run_script("\\Cboe\\", "Cboe_OptionMarketStat_daily.py")
# util.run_script("\\SP500_Ratios\\", "Guru_shiller_sectors.py")   
# ------------MY CODE ----------------------------------

util.log_info("======= Start of daily run =======", 1)

    #----Saturday --------
if util.isToday_Saturday():
    util.run_script("\\Commodity\\", "SHFE_A.py")
    
    util.run_script("\\Commodity\\", "LME_weekly_traderReport.py")    
    # Lithium download only
    util.run_script("\\Commodity\\", "LME_A2.py") 

    # -----FINRA---3ndWeekOfMonth--------
    if util.is_3ndWeekOfMonth_Saturday():
        util.run_script("\\FINRA\\", "FINRA_Margin_Statistics_3ndWeekOfMonth.py")
    pass
    # ---------13F SEC_13F_sina_Stock
    # if util.is_3ndWeekOfMonth_Saturday():
    #     util.run_script("\\SEC_13F\\", "13F SEC_13F_sina_Stock.py")
    
    
#----Thursday --------
# if util.is_COMEX_thursday_run():
# util.run_script("\\Commodity\\", "COMEX_A_gainStock_Tuesday_weekly_Run.py")      
    # pass
    
# if util.is_uk_business_day():
# util.run_script("\\Commodity\\", "LME_daily_openInterest_E.py")     
# util.run_script("\\Commodity\\", "LME_A2.py")
# util.run_script("\\Commodity\\", "LME_daily_volume.py") 
# pass

# if util.is_us_business_day():    
# util.run_script("\\Commodity\\", "COMEX_A.py")      
# util.run_script("\\Commodity\\", "COMEX_daily_openInterest_VOL.py")

#-------cboe
# util.run_script("\\Cboe\\", "Cboe_OptionMarketStat_daily_CbeoOnly.py")
# util.run_script("\\Cboe\\", "Cboe_EquityTrading_ValueVolume_daily.py") 
# util.run_script("\\Cboe\\", "Cboe_OptionMarketStat_daily_Summary_VolNotional.py")

#---other files-------------------------
# util.run_script("\\Fear_Greed\\", "Fear_Greed_CNN.py")   
# util.run_script("\\SP500_Ratios\\", "Guru_shiller_sectors.py")


 
  





