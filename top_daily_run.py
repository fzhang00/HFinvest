"""
Top level python launcher

User must define a few constant: 

_PYTHON : the complete path to your Python exe
_ROOT_DIR: the complete path to the location of this repository
"""

from datetime import datetime
import os
import key as pconst
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
util.log_info("======= Start of daily run =======", 1)
#run_script("\\market_breadth\\", "run.py")

# import SHFE_A as mySHFE_A
# import LME_weekly_traderReport as myLME_weeklyTraderReport

# import LME_A as myLME_A
# import LME_daily_volume as myLME_dailyVol
# import LME_daily_openInterest_E as myLME_daily_openInterest


# import COMEX_A as myCOMEX_A
# import COMEX_daily_openInterest_VOL as myCOMEX_dailyVolOI


#----Saturday --------
if util.isToday_Saturday():
    util.run_script("\\Commodity\\", "SHFE_A.py")
    util.run_script("\\Commodity\\", "LME_weekly_traderReport.py")

#----Thursday --------
if util.is_COMEX_thursday_run:
    util.run_script("\\Commodity\\", "COMEX_A_gainStock_Tuesday_weekly_Run.py")      
    
#----LME daily --------    
if util.is_uk_business_day():
    util.run_script("\\Commodity\\", "LME_A.py")
    util.run_script("\\Commodity\\", "LME_daily_volume.py")    
    util.run_script("\\Commodity\\", "LME_daily_openInterest_E.py")  
    
if util.is_us_business_day():
    util.run_script("\\SP500_Ratios\\", "Guru_shiller_sectors.py")
    # util.run_script("\\Commodity\\", "test.py") 
    
    util.run_script("\\Commodity\\", "COMEX_A.py")      
    util.run_script("\\Commodity\\", "COMEX_daily_openInterest_VOL.py")  


# Schedule monthly tasks. If the scheduled date is a holiday, task will be run on the next business day. US only!
day_on_every_month = 5
if util.is_US_biz_day_of_month(day_on_every_month):
    util.log_info("Running monthly US procedure on day {} of every month".format(day_on_every_month), fname_prefix="monthly_log_")

# Schedule tasks based on fixed day of nth week of certain month. 
# For example, 四巫日, is third Friday of 3,6,9,12 month
day_of_week=4 # Friday
week_of_month=3 # Third week
months=[3,6,9,12]
if util.is_day_of_nweek(day_of_week, week_of_month, months):
    util.log_info("Running tasks for every third Friday of {} months".format(months), fname_prefix="quarterly_log_")


#FINRA generally publishes updates to the Margin Statistics on the third week of the month following the reference month. 
    # # TODO: this to be run monthly
# util.run_script("\\FINRA\\", "FINRA_Margin_Statistics.py")    


    
    # # TODO: 13F is updated quaterly over a few weeks time. Schedule needs special treatment.
    # util.run_script("\\SEC_13F\\", "SEC_13F_sina.py") 

# util.run_script("\\Commodity\\", "COMEX_A_bondsFuture_Delivered_Q_Run.py")  
  





