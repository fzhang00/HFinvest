for /f "tokens=1-4 delims=/ " %%i in ("%date%") do (
     set dow=%%i
     set month=%%j
     set day=%%k
     set year=%%l
)
set datestr=%month%_%day%_%year%
echo datestr is %datestr%

set logfile=daily_run_%datestr%.log
echo log file is %logfile%
@REM Hao's LAPTOP CONFIG
@REM @CALL "C:\ProgramData\Anaconda3\Scripts\activate.bat" C:\ProgramData\Anaconda3
@REM @CALL python G:\Projects\HFinvest\top_daily_run.py  1>daily_run_printout.log 2>&1

@REM Fan's Laptop config

set ROOT_DIR="C:\Users\fzhan\Projects\MyProjects\Investment\HFinvest"
cd %ROOT_DIR%
CALL "C:\Users\fzhan\miniconda3\Scripts\activate.bat" invest
CALL python top_daily_run.py 1>%logfile% 2>&1