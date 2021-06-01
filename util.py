"""
Top level python launcher

User must define a few constant: 

_PYTHON : the complete path to your Python exe
_ROOT_DIR: the complete path to the location of this repository
"""

from datetime import datetime, timedelta
import holidays
import pandas as pd
import subprocess
import os

from pandas.core.indexes.datetimes import date_range
import personal as pconst

_PYTHON = pconst.PYTHON
_ROOT_DIR = pconst.ROOT_DIR

_TODAY = datetime.today()

def log_info(msg, severity=1):
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

def is_not_holiday(date, country='US'):
    """Return True if date is not a holiday in country"""
    local_holidays = holidays.CountryHoliday(country)
    return date not in local_holidays

def is_business_day(date, tz, country):
    """Check if today is a business day. 
    tz is a string specifying timezone. New York is "US/Eastern", London is "GMT"
    """
    # pd.bdate_range return a fixed frequency DatetimeIndex, with business day as the default frequency.
    return bool(len(pd.bdate_range(date, date, tz=tz))) and is_not_holiday(date, country) 

def is_day_of_week(date, day_of_week, check_holiday=False, country='US'):
    """Check if you are on specific day of a week.
        day_of_week: 0 for Monday, 6 is Sunday.
        check_holiday: True -> return false on a holiday, 
        country: 'US', 'UK', 'CA', 'HK'.  
    """
    not_holiday = is_not_holiday(date, country) if check_holiday else True
    return (date.weekday() == day_of_week) and not_holiday

def is_day_of_month(date, day_of_month, check_holiday=False, country='US'):
    """Use this to check if you are on specific day of a month
            day_of_month: 0 for Monday, 6 is Sunday.
            check_holiday: True -> return false on a holiday, 
            country: 'US', 'UK', 'CA', 'HK'
    """
    not_holiday = is_not_holiday(date, country) if check_holiday else True
    return date.day == day_of_month and not_holiday

def is_date(date, date_list, check_holiday=False, country='US'):
    """
    Check if the date is in the date_list.
        date_list: a list of date in string format "YYYY-MM-DD" 
        check_holiday: True -> return false on a holiday, 
        country: 'US', 'UK', 'CA', 'HK'
    """
    # convert date_list to datetime object
    not_holiday = is_not_holiday(date, country) if check_holiday else True
    return (date.strftime("%Y-%m-%d") in date_list) and not_holiday


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
    if is_business_day(_TODAY, timezone):
        run_script(script_folder_name, script_name)
    else:
        log_info("Daily run exit. Not a business day.", 1)

def run_day_of_week(script_folder_name, script_name, day_of_week):
    """Run script on specific day of a week. 0 for Monday, 6 for Sunday"""
    log_info("Running weekly run {}\{}".format(script_folder_name,script_name), 1)
    if is_day_of_week(_TODAY, day_of_week):
        run_script(script_folder_name, script_name)
    else:
        log_info("Weekly run exit. Day not matched.",1)

def run_day_of_month(script_folder_name, script_name, day_of_month):
    """Run script on specific day of a month."""
    log_info("Running monthly run {}\{}".format(script_folder_name,script_name), 1)
    if is_day_of_month(_TODAY, day_of_month):
        run_script(script_folder_name, script_name)
    else:
        log_info("Monthly run exit. Day not matched.",1)    

def run_custom_date(script_folder_name, script_name, date_list):
    """Run script on specific date specified in date_list.
    date_list = ['YYYY-MM-DD', 'YYYY-MM-DD',...]"""
    log_info("Running custom run {}\{}".format(script_folder_name,script_name), 1)
    if is_date(_TODAY, date_list):
        run_script(script_folder_name, script_name)
    else:
        log_info("Custom run exit. Day not matched.",1)     

# --------------------- TOP LEVEL USER FUNCTION -------------------
def is_us_business_day():
    return is_business_day(_TODAY, 'US/Eastern', 'US')

def is_uk_business_day():
    return is_business_day(_TODAY, 'GMT', 'UK')

def is_COMEX_thursday_run(date=_TODAY):
    if is_day_of_week(date-timedelta(days=1), 3) and \
        (not is_not_holiday(date-timedelta(days=1), 'US')):
        # if yesterday is Thursday, and it's a holiday, run COMEX today
        return True
    else:
        # return true if today is Thursday and not a holiday
        return is_day_of_week(date, 3, True, 'US')


#---------------------------TESTING--------------------------------
def test():
    # ---------- Test is_business_day() ---------------
    print("------Test is_business_day()------")
    # this function requires python module holidays
    # pip install holidays
    # China is not available from the holiday module.
    biz_dates_test = {'2020-12-25':[False, 'US/Eastern', 'US'], 
                    '2021-05-31':[False, 'US/Eastern', 'US'],
                    '2021-05-29':[False, 'US/Eastern', 'US'],
                    '2021-05-20':[True, 'US/Eastern', 'US'],
                    '2021-05-03':[False, 'GMT', 'UK'],
                    '2021-05-04':[True, 'GMT', 'UK'],
                    }
    for key, value in biz_dates_test.items():
        is_biz_date = is_business_day(datetime.strptime(key, "%Y-%m-%d"), value[1], value[2])
        print(key, "is a business day?",is_biz_date, ". Correct answer:", value[0])

    # ----------- Run on specific Date -----------------
    print("------Test is_date()------")
    siwu = ['2021-03-19', '2021-06-18', '2021-09-17', '2021-12-17']
    for s in siwu:
        print(s, "is a SIWU day", is_date(datetime.strptime(s, "%Y-%m-%d"), siwu, 
                                             check_holiday=True, country='US'))
    # ----------- Test is_Comex_thusday_run()
    print("------Test is_COMEX_thursday_run()------")
    date_list = [_TODAY - timedelta(days=x) for x in range(8)]
    for d in date_list:
        print(d.strftime("%Y-%m-%d"), "day of the week:", d.weekday(), is_COMEX_thursday_run(d))
if __name__ == "__main__":
    test()
