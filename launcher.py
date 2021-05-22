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



def log_info(msg):
    if os.path.exists(cconst.errorTxtfileName_const):
        append_write = 'a' # append if already exists
    else:
        append_write = 'w' # make a new file if not        
    f = open(cconst.errorTxtfileName_const, append_write)
    f.write('\n'+cconst.now_str + '  error - ' + msg )
    f.close() 

os.chdir(pconst.ROOT_DIR)
schedule = {'sp500': {'app':['\\market_breath\\', 'run.py' ] , 'freq':'daily', 'timezone':'US/Eastern'},
            #'commodity': {'app':['\\Commodity\\', 'comodityDailyRun.py'] , 'freq':'daily', 'timezone':'US/Eastern'},
            # 'day_of_week': 0 for Monday, 6 for Sunday
            'fred1': {'app':['\\FED\\', 'run.py'] , 'freq':'weekly', 'day_of_week':5, 'timezone':'US/Eastern'},
            #'oil1':{'app':'commodity/run.py', 'freq':'04-10', 'timezone':'US/Eastern'},
            #'oil2':{'app':'commodity/run.py', 'freq':'04-10', 'timezone':'Europe/London'}
            }

def is_business_day(date, tz):
    # pd.bdate_range return a fixed frequency DatetimeIndex, with business day as the default frequency.
    return bool(len(pd.bdate_range(date, date, tz=tz)))


# ------------
print("Data downloader launcher")
for (key,app) in schedule.items():
    # key is just a label for human. The program process the content of app. 
    if app['freq']=='daily': # tested
        if is_business_day(datetime.today(), app['timezone']):
            log_info("Running"+  pconst.ROOT_DIR+app['app'][0]+app['app'][1])
            os.chdir(pconst.ROOT_DIR+app['app'][0])
            subprocess.run([pconst.PYTHON, app['app'][1]], shell=True)
            os.chdir(pconst.ROOT_DIR)
    if app['freq']=='weekly': # tested
        if datetime.today().weekday() == app['day_of_week']:
            log_info("Running "+ pconst.ROOT_DIR+app['app'][0]+app['app'][1] + " weekly on "+calendar.day_name[app['day_of_week']])
            os.chdir(pconst.ROOT_DIR+app['app'][0])
            subprocess.run(pconst.PYTHON, app['app'][1]], shell=True)
            os.chdir(pconst.ROOT_DIR)
    if key=='custom':
        for (custom_day, script) in app.items():
            pass

# with open(_ROOT_DIR+'/test_run.txt', 'a+') as f:
#     if is_business_day(datetime.today()):
#         f.write(datetime.now().strftime("%m/%d/%Y, %H:%M:%S")+" Today is a busines day.\n")
#     else:
#         f.write(datetime.now().strftime("%m/%d/%Y, %H:%M:%S")+" Not a business day.\n")