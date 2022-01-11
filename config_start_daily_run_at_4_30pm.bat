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

set ROOT_DIR="G:\Projects\HFinvest\Cboe"
@REM set ROOT_DIR="C:\Users\fzhan\Projects\MyProjects\Investment\HFinvest"
cd %ROOT_DIR%

@REM Hao's LAPTOP CONFIG
@CALL "C:\ProgramData\Anaconda3\Scripts\activate.bat" C:\ProgramData\Anaconda3
@CALL python Cboe_Option_mostActive_CbeoOnly.py 1>%logfile% 2>&1

@REM Fan's Laptop config
@REM CALL "C:\Users\fzhan\miniconda3\Scripts\activate.bat" invest
@REM CALL python top_daily_run.py 1>%logfile% 2>&1