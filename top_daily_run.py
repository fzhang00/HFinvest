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



if util.is_us_business_day():
    util.run_script2("\\Commodity\\", "test.py")  
    # util.run_script("\\Commodity\\", "comodityDailyRun_A.py")    
    # util.run_script("\\SP500_Ratios\\", "Guru_shiller_sectors.py")
    

    # # TODO: 13F is updated quaterly over a few weeks time. Schedule needs special treatment.
    # util.run_script("\\SEC_13F\\", "SEC_13F_sina.py") 


    # # TODO: this to be run monthly
# util.run_script("\\FINRA\\", "FINRA_Margin_Statistics.py")



