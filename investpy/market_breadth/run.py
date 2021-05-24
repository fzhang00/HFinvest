"""
A top level runner that download and update SP500 stock price and market breath. 

To add more tasks to the top runner, import the function and add it to main()
"""

from investpy.market_breath.get_sp500_data import download_Update_SaveData_History_all500
from investpy.market_breath.sp500MarketBread import updateMarketBreadth_SP500Sector, calMA_SP500Sector
from investpy.market_breath.movingAvgCal import overwrite_sp500_prepDirFiles
import os
import investpy.market_breath.sp500Const as const

def main():
    if not os.path.exists(const.sp500dataWorkingDir_const):
        os.mkdir(const.sp500dataWorkingDir_const)
    print("call download_Update_SaveData_History_all500")
    download_Update_SaveData_History_all500 (const.sp500Info_file_const)
    calMA_SP500Sector(maDay_int = 20, logOn = False)
    overwrite_sp500_prepDirFiles()
    updateMarketBreadth_SP500Sector(20)



if __name__ == "__main__":
    main()