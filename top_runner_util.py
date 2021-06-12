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
_US_HOLIDAYS=['2021-01-01', '2021-01-18', '2021-02-15', '2021-04-02', '2021-05-31', '2021-07-05', '2021-09-06', '2021-11-25', '2021-12-24',
              '2022-01-17', '2022-02-21', '2022-04-15', '2022-05-30', '2022-07-04', '2022-09-05', '2022-11-24', '2022-12-26',
              '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-07-04', '2023-09-04', '2023-11-23', '2023-12-26']

def log_info(msg, fname_prefix="daily_log_", severity=1):
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
    """Check if today is a business day. 
    tz is a string specifying timezone. New York is "US/Eastern", London is "GMT"
    """
    # pd.bdate_range return a fixed frequency DatetimeIndex, with business day as the default frequency.
    try:
        return bool(len(pd.bdate_range(date, date, tz=tz))) and is_not_holiday(date, country) 
    except ValueError:
        return False

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

# --------------------- TOP LEVEL USER FUNCTION -------------------
# def isToday_weekend():
#     dd = datetime.today()
#     result = ( (dd.weekday() == 5) or  (dd.weekday() == 6) )
#     return result
def is_US_biz_day_of_month(day_number, datein=_TODAY):
    """Return True for US day of month. If that day is a holiday, return True the next day
    """
    # get previous schedule date
    if datein.day>day_number:
        previous_schedule=ddate(datein.year, datein.month, day_number)
    elif datein.day<day_number: # previous schedule is previous month
        try:
            previous_schedule=ddate(datein.year, datein.month-1, day_number)
        except ValueError:
            previous_schedule=None # previous month doesn't have that day
    else: previous_schedule=None #datein.day==day_number, let is_day_of_month handle it.
    #
    if (previous_schedule is not None) and (not is_business_day(previous_schedule, "US/Eastern", "US")): # if previous schedule is not a business day5
        if len(pd.bdate_range(previous_schedule, datein, tz='US/Eastern', freq='C', holidays=_US_HOLIDAYS, weekmask='1111100'))==1 and \
            (is_not_holiday(datein)):# datein is the first business day after schedule
            log_info("\t Matched first business day {} for schedule {}".format(datein.date(), previous_schedule),fname_prefix="monthly_log")
            return True
        else:
            return False
    # Return True if day match and is business day
    elif is_day_of_month(datein, day_number, check_holiday=True, country='US') and is_business_day(datein, "US/Eastern", 'US'):
        log_info("/t Matched {} day of {} month".format(day_number, datein.month), fname_prefix="monthly_log")
        return True
    else:
        # this is the day but could be a holiday or weekend, add the next business day as run schedule
        return False

def is_day_of_nweek(day, week, month, datein=_TODAY):
    """Return True for certain day of nth week for every month. 
    Example, every third friday of every month would be is_day_of_nweek(4,3)
    """
    if week==3:
        return datein.weekday() == day and 15 <= datein.day <= 21 and datein.month==month
    elif week==2:
        return datein.weekday() == day and 8 <= datein.day <= 14 and datein.month==month
    elif week==1:
        return datein.weekday() == day and 1 <= datein.day <= 7 and datein.month==month
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

def is_COMEX_thursday_run(date=_TODAY):
    day_of_week=3
    if is_day_of_week(date-timedelta(days=1), day_of_week) and \
        (not is_not_holiday(date-timedelta(days=1), 'US')):
        # if yesterday is Thursday, and it's a holiday, run COMEX today
        return True
    else:
        # return true if today is Thursday and not a holiday
        return is_day_of_week(date, day_of_week, True, 'US')


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
    date_list = [_TODAY - timedelta(days=x) for x in range(8)]
    for d in date_list:
        print(d.strftime("%Y-%m-%d"), "day of the week:", d.weekday(), is_COMEX_thursday_run(d))

    # ----------- Test is_US_day_of_month()---------
    print("-------Test is_US_day_of_month ----------")
    date_list = [datetime.strptime('2021-05-25', "%Y-%m-%d")+timedelta(days=x) for x in range(10)]
    for d in date_list:
        print(d.strftime("%Y-%m-%d"), "is business day for 31 of month", is_US_biz_day_of_month(31, d))

    # ---------- Test third friday of every quater 2021---------------------
    print("-------- Test third Friday of last month of a quarter ---------")
    siwu = ['2021-03-19', '2021-06-18', '2021-09-17', '2021-12-17', '2021-03-12', '2021-06-25']
    months=[3,6,9,12, 3, 6]
    for (s,m) in zip(siwu, months):
        datein=datetime.strptime(s, "%Y-%m-%d")
        print(s, "is third Friday of {} month".format(m), is_day_of_nweek(4, 3, m, datein=datein))
if __name__ == "__main__":
    test()
