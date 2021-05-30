"""
This version of launcher uses subprocess to run subfolder Python script. 

User must define the schedule in a dictionary:
    schedule = {schedule_name: {'app':path_to_script, 
                                'freq':<choose from 'daily', 'weekly', 'monthly', 'custom'>,
                                'day_of': <for weekly, enter the day of the week in number,
                                           for monthly, enter the day of the month in number,
                                           for custom, enter the specific day>,
                                'timezone': Enter the timezone in text. For north america, use 'US/Eastern'}}
    - subfolder name and the python script name
    - How frequent do you want to run this file. Choises are daily, weekly, or custom
        - If weekly, you can specify which day of the week to run the script, by dictionary key
"""



schedule = {'sp500': {'app':['\\market_breath\\', 'run.py' ] , 'freq':'daily', 'timezone':'US/Eastern'},
            #'commodity': {'app':['\\Commodity\\', 'comodityDailyRun.py'] , 'freq':'daily', 'timezone':'US/Eastern'},
            # 'day_of_week': 0 for Monday, 6 for Sunday
            'fred1': {'app':['\\FED\\', 'run.py'] , 'freq':'weekly', 'day_of_week':5, 'timezone':'US/Eastern'},
            #'oil1':{'app':'commodity/run.py', 'freq':'04-10', 'timezone':'US/Eastern'},
            #'oil2':{'app':'commodity/run.py', 'freq':'04-10', 'timezone':'Europe/London'}
            }

import argparse
from datetime import datetime
import pandas as pd
import subprocess
import os
import calendar
import const_common as const

_PYTHON = 'C:\\Users\\fzhan\\miniconda3\\envs\\invest\\python.exe'
_ROOT_DIR = "c:\\Users\\fzhan\\Projects\\MyProjects\\Investment\\HFinvest"

today = datetime.today()

def log_info(msg, severity):
    """ Log message into launcher log, filename patterh: launcher_subproc_log_<date>.log

    Input:
        - msg: str, the text message you want to include to the log,
        - severity: int, the type of message. 3 for ERROR, 2 for DEBUG, 1 for INFO
    """
    _LOG_TYPE = {1:'INFO', 2:'DEBUG',3:'ERROR'}
    now = datetime.today()
    fname = "./log/launcher_subproc_log_{}.log".format(now.strftime("%Y-%m-%d"))
    if os.path.exists(fname):
        append_write = 'a' # append if already exists
    else:
        append_write = 'w' # make a new file if not        
    f = open(fname, append_write)
    f.write('\n'+now.strftime("%Y-%m-%d %H:%M:%S") + '  {} - '.format(_LOG_TYPE[severity]) + msg )
    f.close() 




def is_business_day(date, tz):
    """Check if today is a business day. 
    tz is a string specifying timezone. New York is US/Eastern"""
    # pd.bdate_range return a fixed frequency DatetimeIndex, with business day as the default frequency.
    return bool(len(pd.bdate_range(date, date, tz=tz)))

def is_day_of_week(date, day_of_week):
    """Check if you are on specific day of a week.
    0 for Monday, 6 is Sunday."""
    return date.weekday() == day_of_week

def is_day_of_month(date, day_of_month):
    """Use this to check if you are on specific day of a month"""
    return date.day == day_of_month

def is_date(date, date_list):
    # convert date_list to datetime object
    if date.strftime("%Y-%m-%d") in date_list:
        return True
    else:
        return False

def run_script(script_folder_name, script_name):
    """Run script with exception handling"""
    try:
        os.chdir(_ROOT_DIR+script_folder_name)
        print(os.getcwd())
        subprocess.run([_PYTHON, script_name], shell=True)
    except Exception as e:
        print(e)
        #log_info(e, 3)
    finally:
        os.chdir(_ROOT_DIR)

def run_daily(script_folder_name, script_name, timezone):
    """Run script on every business day"""
    log_info("Running daily run {}\{}".format(script_folder_name,script_name), 1)
    if is_business_day(today, timezone):
        run_script(script_folder_name, script_name)
    else:
        log_info("Daily run exit. Not a business day.", 1)

def run_day_of_week(script_folder_name, script_name, day_of_week):
    """Run script on specific day of a week. 0 for Monday, 6 for Sunday"""
    log_info("Running weekly run {}\{}".format(script_folder_name,script_name), 1)
    if is_day_of_week(today, day_of_week):
        run_script(script_folder_name, script_name)
    else:
        log_info("Weekly run exit. Day not matched.",1)

def run_day_of_month(script_folder_name, script_name, day_of_month):
    """Run script on specific day of a month."""
    log_info("Running monthly run {}\{}".format(script_folder_name,script_name), 1)
    if is_day_of_month(today, day_of_month):
        run_script(script_folder_name, script_name)
    else:
        log_info("Monthly run exit. Day not matched.",1)    

def run_custom_date(script_folder_name, script_name, date_list):
    """Run script on specific date specified in date_list.
    date_list = ['YYYY-MM-DD', 'YYYY-MM-DD',...]"""
    log_info("Running custom run {}\{}".format(script_folder_name,script_name), 1)
    if is_date(today, date_list):
        run_script(script_folder_name, script_name)
    else:
        log_info("Custom run exit. Day not matched.",1)     
# ------------
print("Data downloader launcher")
os.chdir(_ROOT_DIR)
# ----------- List your script here:

# use run_daily() to run script on every business day
#run_daily("\\Commodity\\", "commodityDailyRun_A.py", 'US/Eastern')

# use run_script() to run any script regardless of the timec:\Users\fzhan\Projects\MyProjects\Investment\HFinvest\Commodity\data\Shanghai\temp\2021-05-28\ShanghaiStock_weekly.csv.html

run_script("\\market_breadth\\", "run.py")
#run_script("\\Commodity\\", "comodityDailyRun_A.py")
# run_day_of_week()





# for (key,app) in schedule.items():
#     # key is just a label for human. The program process the content of app. 
#     if app['freq']=='daily': # tested
#         if is_business_day(datetime.today(), app['timezone']):
#             log_info("Running"+  _ROOT_DIR+app['app'][0]+app['app'][1])
#             os.chdir(_ROOT_DIR+app['app'][0])
#             subprocess.run([_PYTHON, app['app'][1]], shell=True)
#             os.chdir(_ROOT_DIR)
#     if app['freq']=='weekly': # tested
#         if datetime.today().weekday() == app['day_of_week']:
#             log_info("Running "+ _ROOT_DIR+app['app'][0]+app['app'][1] + " weekly on "+calendar.day_name[app['day_of_week']])
#             os.chdir(_ROOT_DIR+app['app'][0])
#             subprocess.run([_PYTHON, app['app'][1]], shell=True)
#             os.chdir(_ROOT_DIR)
#     if key=='custom':
#         for (custom_day, script) in app.items():
#             pass

