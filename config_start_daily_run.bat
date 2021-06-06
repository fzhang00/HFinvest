REM Hao's LAPTOP CONFIG
@REM @CALL "C:\ProgramData\Anaconda3\Scripts\activate.bat" C:\ProgramData\Anaconda3
@REM @CALL python G:\Projects\HFinvest\top_daily_run.py  1>daily_run_printout.log 2>&1

REM Fan's Laptop config
@ECHO OFF
set ROOT_DIR="C:\Users\fzhan\Projects\MyProjects\Investment\HFinvest"
cd %ROOT_DIR%
@CALL "C:\Users\fzhan\miniconda3\Scripts\activate.bat" invest
@CALL python top_daily_run.py 1>daily_run_printout.log 2>&1