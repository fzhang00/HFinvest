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
from investpy.market_breadth.run import *
from investpy.Commodity.comodityDailyRun_A import *
from investpy.SP500_Ratios.Guru_shiller_sectors import *
from investpy.FINRA.FINRA_Margin_Statistics import html_monthly_3ndWeek_Margin_Statistics


def is_business_day(date, tz):
    """Return True if it is a business day in tz timezone"""
    # pd.bdate_range return a fixed frequency DatetimeIndex, with business day as the default frequency.
    return bool(len(pd.bdate_range(date, date, tz=tz)))

def is_weekend(date):
    """Return True if it is a weekend"""
    return ( (date.weekday() == 5) or  (date.weekday() == 6) )


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

# ------------
print("Data downloader launcher")

# Run on every business day
if is_business_day(datetime.today(), tz='US/Eastern'):
    print("Running tasks on every business day.")
    daily_market_breadth() # run sp500 market breadth
    daily_runCommodity() # run commodity
    sp500_daily_run_PE() # run shiller ratio
    html_monthly_3ndWeek_Margin_Statistics()

# Run on weekend
if is_weekend(datetime.today()):
    print("Running tasks on weekend")
    weekend_runCommodity()







