"""
Top level python launcher

User must define a few constant: 

_PYTHON : the complete path to your Python exe
_ROOT_DIR: the complete path to the location of this repository
"""

from datetime import datetime, timedelta
from datetime import date as ddate
import holidays
import pandas as pd
import subprocess
import os

from pandas.core.indexes.datetimes import date_range
import key as pconst

_TODAY = datetime.today()


# _US_HOLIDAYS=['2021-01-01', '2021-01-18', '2021-02-15', '2021-04-02', '2021-05-31', '2021-07-05', '2021-09-06', '2021-11-25', '2021-12-24',
#               '2022-01-17', '2022-02-21', '2022-04-15', '2022-05-30', '2022-07-04','2022-07-05', '2022-09-05', '2022-11-24', '2022-12-26',
#               '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-07-04', '2023-09-04', '2023-11-23', '2023-12-26']

def log_info(msg, severity=1, fname_prefix="daily_log_"):
    """ Log message into launcher log, filename patter: daily_log_<date>.log

    Input:
        - msg: str, the text message you want to include to the log,
        - severity: int, the type of message. 3 for ERROR, 2 for DEBUG, 1 for INFO
    """
    _LOG_TYPE = {1:'INFO', 2:'DEBUG',3:'ERROR'}
    now = datetime.today()
    fname = "./log/"+fname_prefix+"{}.log".format(now.strftime("%Y-%m-%d"))
    if os.path.exists(fname):
        append_write = 'a' # append if already exists
    else:
        append_write = 'w' # make a new file if not        
    f = open(fname, append_write)
    log_msg='\n'+now.strftime("%Y-%m-%d %H:%M:%S") + '  {} - '.format(_LOG_TYPE[severity]) + msg 
    f.write(log_msg)
    print(log_msg)
    f.close() 

def is_not_holiday(date, country='US'):
    """Return True if date is not a holiday in country"""
    local_holidays = holidays.CountryHoliday(country)
    return date not in local_holidays

def is_business_day(date, tz, country):
    """Check if today is a business day, ie. not a weekend and not a holiday. 
    tz: a string specifying timezone. New York is "US/Eastern", London is "GMT"
    """
    # pd.bdate_range return a fixed frequency DatetimeIndex, with business day as the default frequency.
    try:
        return bool(len(pd.bdate_range(date, date, tz=tz))) and is_not_holiday(date, country) 
    except ValueError:
        return False

def _find_biz_day(date, tz, country, next=True):
    """Get the next business day of a date.
    
    If next is True: find the next business day including the input date.
    If next is False: find the previous business day starting from input date - 1 day"""
    check_biz_day = date if next else date-timedelta(days=1)
    while not is_business_day(check_biz_day, tz, country):
        if next: 
            check_biz_day += timedelta(days=1)
        else:
            check_biz_day -= timedelta(days=1)
    return check_biz_day

_PREV_BIZ_DAY_US = _find_biz_day(_TODAY, 'US/Eastern', 'US', False)
_PREV_BIZ_DAY_UK = _find_biz_day(_TODAY, 'GMT', 'UK', False)

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
        log_info("Running run {}\{}".format(script_folder_name,script_name), 1)
        os.chdir(os.path.join(os.getcwd()+script_folder_name))
        proc = subprocess.run(['python', script_name],stdout=subprocess.PIPE, universal_newlines=True, shell=True)
        print (proc.stdout)
    except Exception as e:
        log_info(str(e), 3)
        print(e)        
    finally:
        os.chdir("..")
        
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

def is_day_of_nweek(day, week, months, datein=_TODAY):
    """Return True for certain day of nth week for every month. 
    Example, every third friday of every month would be is_day_of_nweek(4,3)
    
    Input: 
        day: day of the week, 0 for Monday, 6 for Sunday
        week: nth week of the month, 1, 2, or 3
        months: list, a list of months number to match. ie： [3,6,9,12]
    """
    if week==3:
        return datein.weekday() == day and 15 <= datein.day <= 21 and datein.month in months
    elif week==2:
        return datein.weekday() == day and 8 <= datein.day <= 14 and datein.month in months
    elif week==1:
        return datein.weekday() == day and 1 <= datein.day <= 7 and datein.month in months
    else:
        print("Number of week not supported")
        return False

def isToday_Saturday():
    dd = datetime.today()
    return (dd.weekday() == 5)

def is_us_business_day():
    return is_business_day(_TODAY, 'US/Eastern', 'US')

def is_uk_business_day():
    return is_business_day(_TODAY, 'GMT', 'UK')

# TODO Auto download and check based on Comex holiday. This checker only based on federal US holiday. 
def is_COMEX_thursday_run(date=_TODAY):
    return biz_weekday_run_US(date, 3)

def biz_weekday_run_US(day_of_week, date=_TODAY, prev=_PREV_BIZ_DAY_US):
    """Given day of week, return True/False if it should be run on the input date. 
    If the day_of_week was a holiday, function should return true on the next business day. """

    if is_business_day(date, 'US/Eastern', 'US'): # check for business day and holiday
        if is_day_of_week(date, day_of_week): # on the right day
            # return True if this is the date, and its not a holiday, else return False
            return True
        else:  # Run on the next biz day if schedule date is holiday

            if date.weekday()<prev.weekday():
                _this_weekday = date.weekday()+7
            else:
                _this_weekday = date.weekday()
            if prev.weekday()<day_of_week and _this_weekday>day_of_week:
                return True
            else: 
                return False
    else:
        return False

# def biz_weekly_run_US(date, day_of_week):# Fan
    # if not is_day_of_week(date, day_of_week):
    #     if date.weekday()<day_of_week:
    #         day_diff = date.weekday()+7-day_of_week
    #     else:
    #         day_diff = date.weekday()-day_of_week
    #     prev_schedule = date - timedelta(days=day_diff)
    #     next_biz_day = _find_biz_day(prev_schedule, 'US/Eastern', 'US')
    #     return (date-next_biz_day).days==0
    # else:
    #     return is_day_of_week(date, day_of_week, True, 'US')

def biz_monthly_US_run(date, day_of_month):
    """Given day of month, return True/False if it should be run on the input date. 
    If the day_of_week was a holiday, function should return true on the next business day. """
    if day_of_month > 25:
        log_info("Maximum day of month accepted is 25", severity=3)
        raise("Error: Maximum day of month accepted is 25")
    _prev = _find_biz_day(date, 'US/Eastern', 'US', False)
    if is_business_day(date, 'US/Eastern', 'US'): # check for business day and holiday
        if is_day_of_month(date, day_of_month): # on the right day
            # return True if this is the date, and its not a holiday, else return False
            return True
        else:
            if _prev.day<day_of_month and date.day>day_of_month:
                return True
            else: 
                return False
    else:
        return False

def biz_monthly_US_run_fan(date, day_of_month): # Fan
    """Given day of month, return True/False if it should be run on the input date. 
    If the day_of_month was a holiday, function should return True on the next business day. """
    # Don't want to handle variable month end date
    if day_of_month > 28:
        log_info("Maximum day of month accepted is 28", severity=3)
        raise("Error: Maximum day of month accepted is 28")
    # Main Logic
    if is_business_day(date, 'US/Eastern', 'US'): # it is a business day
        if is_day_of_month(date, day_of_month): # it is the right calender date
            return True
        else: # it is a business day but not the scheduled calender date
            if date.day<day_of_month: # The month has rolled over
                month = 12 if date.month==1 else date.month-1
                prev_schedule = datetime(date.year, month, day_of_month)
            else: # same month
                prev_schedule = datetime(date.year, date.month, day_of_month)
            next_biz_day = _find_biz_day(prev_schedule, 'US/Eastern', 'US')
            return (date-next_biz_day).days==0
    else:
        return False
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
    print("None is a business day?", is_business_day(None, "US/Eastern", "US"))
    # ----------- Run on specific Date -----------------
    print("------Test is_date()------")
    siwu = ['2021-03-19', '2021-06-18', '2021-09-17', '2021-12-17']
    for s in siwu:
        print(s, "is a SIWU day", is_date(datetime.strptime(s, "%Y-%m-%d"), siwu, 
                                             check_holiday=True, country='US'))
    # ----------- Test is_Comex_thusday_run()
    print("------Test is_COMEX_thursday_run()------")
    date_list = [datetime.strptime('2021-11-22', "%Y-%m-%d") + timedelta(days=x) for x in range(8)]
    for d in date_list:
        print(d.strftime("%Y-%m-%d"), "day of the week:", d.weekday(), is_COMEX_thursday_run(d))

    # ----------- Test is_US_day_of_month()---------
    print("-------Test is_US_day_of_month ----------")
    date_list = [datetime.strptime('2021-12-23', "%Y-%m-%d")+timedelta(days=x) for x in range(10)]
    for d in date_list:
        print(d.strftime("%Y-%m-%d"), "is business day for 25 of month", biz_monthly_US_run(d, 25))

    # ---------- Test third friday of every quater 2021---------------------
    print("-------- Test third Friday of last month of a quarter ---------")
    siwu = ['2021-03-19', '2021-06-18', '2021-09-17', '2021-12-17', '2021-03-12', '2021-06-25']
    months=[3,6,9,12]
    for s in siwu:
        datein=datetime.strptime(s, "%Y-%m-%d")
        print(s, "is third Friday of {} month".format(months), is_day_of_nweek(4, 3, months, datein=datein))
if __name__ == "__main__":
    test()
