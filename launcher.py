"""
This file manages the automatic run. To use this script, you need to define a personal.py file.
In personal.py file, you need to define: 
    PYTHON='path_to_your_python_exe'
    ROOT_DIR='path_to_your_HFinvest_directory' 
"""
from datetime import datetime
import pandas as pd
import subprocess
import os
import calendar
import const_common as cconst
import personal as pconst
from investpy.market_breath.run import main as run_sp500
from investpy.Commodity.comodityDailyRun_A import daily_runCommodity as run_commodity



def log_info(msg):
    if os.path.exists(cconst.errorTxtfileName_const):
        append_write = 'a' # append if already exists
    else:
        append_write = 'w' # make a new file if not        
    f = open(cconst.errorTxtfileName_const, append_write)
    f.write('\n'+cconst.now_str + '  error - ' + msg )
    print(msg)
    f.close() 

os.chdir(pconst.ROOT_DIR)
schedules = {'sp500': {'app':run_sp500, 'freq':'daily', 'timezone':'US/Eastern'},
             'commodity': {'app':run_commodity, 'freq':'daily', 'timezone':'US/Eastern'},
            # 'day_of_week': 0 for Monday, 6 for Sunday
            #'fred1': {'app':['\\FED\\', 'run.py'] , 'freq':'weekly', 'day_of_week':5, 'timezone':'US/Eastern'},
            #'oil1':{'app':'commodity/run.py', 'freq':'04-10', 'timezone':'US/Eastern'},
            #'oil2':{'app':'commodity/run.py', 'freq':'04-10', 'timezone':'Europe/London'}
            }

def is_business_day(date, tz):
    # pd.bdate_range return a fixed frequency DatetimeIndex, with business day as the default frequency.
    return bool(len(pd.bdate_range(date, date, tz=tz)))

# ------------
print("Data downloader launcher")
for (name,schedule) in schedules.items():
    # key is just a label for human. The program process the content of app. 
    if schedule['freq']=='daily': # tested
        if is_business_day(datetime.today(), schedule['timezone']):
            log_info("Runing "+name)
            schedule['app']()
    if schedule['freq']=='weekly': # tested
        if datetime.today().weekday() == schedule['day_of_week']:
            schedule['app']()
    if name=='custom':
        for (custom_day, script) in schedule.items():
            pass

# with open(_ROOT_DIR+'/test_run.txt', 'a+') as f:
#     if is_business_day(datetime.today()):
#         f.write(datetime.now().strftime("%m/%d/%Y, %H:%M:%S")+" Today is a busines day.\n")
#     else:
#         f.write(datetime.now().strftime("%m/%d/%Y, %H:%M:%S")+" Not a business day.\n")