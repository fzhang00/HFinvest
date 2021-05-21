"""
A top level runner that download and update SP500 stock price and market breath. 

To add more tasks to the top runner, import the function and add it to main()
"""

from get_sp500_data import download_Update_SaveData_History_all500
from sp500MarketBread import updateMarketBreadth_SP500Sector
import os
import sp500Const as const

def main():
    if not os.path.exists(const.sp500dataWorkingDir_const):
        os.mkdir(const.sp500dataWorkingDir_const)
    print("call download_Update_SaveData_History_all500")
    download_Update_SaveData_History_all500 (const.sp500Info_file_const)
    updateMarketBreadth_SP500Sector(20)

if __name__ == "__main__":
    main()