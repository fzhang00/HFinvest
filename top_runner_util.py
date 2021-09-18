"""
This module provides a list of utility functions for scheduling investment data download tasks. 

All internal functions start with _ in its name. 

For all top level functions, scroll down to the function to see its documentation. 

Top level function list: 
    - run_script: start a subprocess to run script.
    - Scheduler functions: 
        - is_business_day: Check if a date is a business day, ie. not weekend or holiday
        - is_day_of_week: Check if a date is specific day of week, ie: Monday, Thursday, etc
        - is_day_of_month: Check if a date is specific day of a month, ie: 15th, 21th
        - is_date: Check if a date matches a list of calender date given in the date_list
        - is_day_of_nweek: Check if a date matches specific weekday of nth week in a list of monthes. ie. third Friday of monthes [3,6,9,12]
        - isToday_Saturday: Check if a date is Saturday
        - is_us_business_day: Check if a date is US business day, ie. not weekend or federal holiday.
        - is_uk_business_day: Check if a date is UK business day.
        - biz_weekday_run_US: Check if a date matches the specified weekday for US market. This function can be used to schedule weekly US market tasks. If the specified weekday is a holiday, the function will return True on the next business day following the holiday. 
        - biz_weekday_run_UK: Same as biz_weekday_run_US, but for UK market.
        - biz_weekday_run: Same as the biz_weekday_run_US, but user can specify timezone and country.
        - biz_monthly_run_US: Check if a date matches the specified day of month on US market. If the specified day of month is a holiday, the function returns True on the next business day following the holiday. 
        - biz_monthly_run_UK: Same as biz_monthly_run_US, but for UK market.
        - biz_montly_run: Same as biz_monthly_run_US. User can specify time zone and country.
        - biz_date_run_US: Check if a date matches the specified list of calender date. If the specified date is a holiday, the function returns True on the next business day following the holiday. 
        - biz_date_run_UK: Same as biz_date_run_US, but for UK market.
        - biz_date_run: Same as biz_date_run_US, but user can specify time zone and country. 
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

def run_script(script_folder_name, script_name):
    """Run script with exception handling. Raised error is logged into ./log/daily_log_YY-mm-dd.log
    
    Inputs:
        script_folder_name: script folder name related to project top folder
        script_name: python script name."""
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

def _is_not_holiday(date, country='US'):
    """Return True if date is not a holiday in country"""
    local_holidays = holidays.CountryHoliday(country)
    return date not in local_holidays

def is_business_day(date, tz, country):
    """Check if today is a business day, ie. not a weekend and not a holiday. 
    tz: a string specifying timezone. New York is "US/Eastern", London is "GMT"
    """
    # pd.bdate_range return a fixed frequency DatetimeIndex, with business day as the default frequency.
    try:
        return bool(len(pd.bdate_range(date, date, tz=tz))) and _is_not_holiday(date, country) 
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

def _validate_biz_day_post_holiday(today, prev, target):
    """Return True if target day falls in between 
    previous business day and today(business day)."""
    # print(f"today:{today}, prev:{prev}, target:{target}") # DEBUG print
    if prev<target and today>target:
        return True
    else:
        return False

def is_day_of_week(date, day_of_week):
    """Check if you are on specific day of a week.
        day_of_week: 0 for Monday, 6 is Sunday.
    """
    return (date.weekday() == day_of_week)

def is_day_of_month(date, day_of_month):
    """Use this to check if you are on specific day of a month."""
    return date.day == day_of_month

def is_date(date, date_list):
    """
    Check if the date is in the date_list.
        date_list: a list of date in string format "YYYY-MM-DD" 
    """
    return (date.strftime("%Y-%m-%d") in date_list)

def is_day_of_nweek(day, week, months, datein=_TODAY):
    """Return True for certain day of nth week for input months.
    This function does NOT check for business day or holiday. 

    Example, every third friday of month 3,6,9,12 would be is_day_of_nweek(4,3, [3,6,9,12])
    
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

def isToday_Saturday(date=_TODAY):
    return (date.weekday() == 5)

def is_us_business_day(date=_TODAY):
    return is_business_day(date, 'US/Eastern', 'US')

def is_uk_business_day(date=_TODAY):
    return is_business_day(date, 'GMT', 'UK')

def biz_weekday_run_US(day_of_week, date=_TODAY, prev=_PREV_BIZ_DAY_US):
    """US weekly run on business day. Return True/False.
    
    Example: to check if today is Thursday of every week,
    ```python
    if biz_weekday_run_US(3):
        run_script('script folder', 'script')
    ```
    """
    return biz_weekday_run(day_of_week, date, prev, 'US/Eastern', 'US')

def biz_weekday_run_UK(day_of_week, date=_TODAY, prev=_PREV_BIZ_DAY_US):
    """UK weekly run on business day. Return True/False """
    return biz_weekday_run(day_of_week, date, prev, 'GMT', 'UK')

def biz_weekday_run(day_of_week, date, prev, tz, country):
    """Given day of week, return True/False if it should be run on the input date. 
    If the day_of_week was a holiday, function should return true on the next business day. 
    
    Input: 
        - day_of_week: int, number representing the day of week: 0 for Monday, 6 for Saturday
        - date: input date to check for. 
        - prev: previous business day from the input date. use _find_biz_day()
        - tz: str, describing the time zone.
        - country: str, describing the country. """

    if is_business_day(date, tz, country): # check for business day and holiday
        if is_day_of_week(date, day_of_week): # on the right day
            return True
        else:  # Run on the next biz day if schedule date is holiday
            if date.weekday()<prev.weekday():
                _this_weekday = date.weekday()+7
            else:
                _this_weekday = date.weekday()
            return _validate_biz_day_post_holiday(_this_weekday, prev.weekday(), day_of_week)
    else:
        return False

def biz_monthly_run_US(day_of_month, date=_TODAY, prev=_PREV_BIZ_DAY_US):
    """US monthly run on business day. Return True/False.
    
    Example: to check if today is 15th of each month: 
    ```python
    if biz_montly_run_US(15):
        run_script('script_folder', 'script')
    ```
    """
    return biz_monthly_run(day_of_month, date, prev, 'US/Eastern', 'US')

def biz_monthly_run_UK(day_of_month, date=_TODAY, prev=_PREV_BIZ_DAY_UK):
    """US monthly run on business day. Return True/False """
    return biz_monthly_run(day_of_month, date, prev, 'GMT', 'UK')

def biz_monthly_run(day_of_month, date, prev, tz, country):
    """Given day of month, return True/False if it should be run on the input date. 
    If the day_of_week was a holiday, function should return true on the next business day. 
        
    Input: 
        - day_of_month: int, number representing the day of month
        - date: input date to check for. 
        - prev: previous business day from the input date. use _find_biz_day()
        - tz: str, describing the time zone.
        - country: str, describing the country. """
    if day_of_month > 25:
        log_info("Maximum day of month accepted is 25", severity=3)
        raise("Error: Maximum day of month accepted is 25")
    if is_business_day(date, tz, country): # check for business day and holiday
        if is_day_of_month(date, day_of_month): # on the right day
            return True
        else:
            return _validate_biz_day_post_holiday(date.day, prev.day, day_of_month)
    else:
        return False

def biz_date_run_US(date_list, date=_TODAY, prev=_PREV_BIZ_DAY_US):
    """US custom date run on business day. Return True/False """
    return biz_date_run(date_list, date, prev, 'US/Eastern', 'US')

def biz_date_run_UK(date_list, date=_TODAY, prev=_PREV_BIZ_DAY_UK):
    """US custom date run on business day. Return True/False """
    return biz_date_run(date_list, date, prev, 'GMT', 'UK')

def biz_date_run(date_list, date, prev, tz, country):
    """Given a list of calender date string in "%Y-%m-%d format, return True/False if it should be run on the input date. 

    If the schedule date was a holiday, function should return true on the next business day. 
        
    Input: 
        - date_list: a list of "%Y-%m-%d string
        - date: input date to check for. 
        - prev: previous business day from the input date. use _find_biz_day()
        - tz: str, describing the time zone.
        - country: str, describing the country. 
"""
    if is_business_day(date, tz, country ):
        if is_date(date, date_list):
            return True
        else: # this is not a scheduled date
            targets = [datetime.strptime(d, "%Y-%m-%d") for d in date_list] 
            for t in targets:
                if t.month==date.month:
                    if prev.day<t.day:
                        return _validate_biz_day_post_holiday(date.day, prev.day, t.day)
                else:
                    return False
    else:
        return False

# TODO Auto download and check based on Comex holiday. This checker only based on federal US holiday. 
def is_COMEX_thursday_run(date=_TODAY):
    return biz_weekday_run_US(date, 3)
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
    print("------Test biz_date_US_run------")
    target_list = ['2021-12-17', '2021-12-25']
    input_list = [datetime.strptime('2021-12-15', "%Y-%m-%d")+timedelta(days=x) for x in range(22)]
    for d in input_list:
        print(d.strftime("%Y-%m-%d"), "matches", target_list, 
              biz_date_run_US(target_list, d, _find_biz_day(d, 'US/Eastern', 'US', False)))
    # ----------- Test is_Comex_thusday_run()
    print("------Test is_COMEX_thursday_run()------")
    date_list = [datetime.strptime('2021-11-22', "%Y-%m-%d") + timedelta(days=x) for x in range(8)]
    for d in date_list:
        print(d.strftime("%Y-%m-%d"), "day of the week:", d.weekday(),
              biz_weekday_run_US(3,d,_find_biz_day(d, 'US/Eastern', 'US', False)))

    # ----------- Test is_US_day_of_month()---------
    print("-------Test is_US_day_of_month ----------")
    date_list = [datetime.strptime('2021-12-23', "%Y-%m-%d")+timedelta(days=x) for x in range(10)]
    for d in date_list:
        print(d.strftime("%Y-%m-%d"), "is business day for 25 of month", 
              biz_monthly_run_US(25, d, _find_biz_day(d, 'US/Eastern', 'US', False)))

    # ---------- Test third friday of every quater 2021---------------------
    print("-------- Test third Friday of last month of a quarter ---------")
    siwu = ['2021-03-19', '2021-06-18', '2021-09-17', '2021-12-17', '2021-03-12', '2021-06-25']
    months=[3,6,9,12]
    for s in siwu:
        datein=datetime.strptime(s, "%Y-%m-%d")
        print(s, "is third Friday of {} month".format(months), is_day_of_nweek(4, 3, months, datein=datein))
if __name__ == "__main__":
    test()
