import pandas as pd
import os.path as myPath

import sp500Const as const
import get_sp500_data as getDateFrame
from numpy import floor
import glob
#------------------------------ 

def calMA_SP500Sector(maDay_int, logOn):
    
    df      = pd.read_csv(const.sp500Info_file_const)
    df_array = df['GICS Sector'].unique()
    

    for i in range(len(df_array)):
        print(df_array[i] + "-------") # 11 sectors
        
        sectorFilePath = const.sp500_sectorsDir_const + "/" + df_array[i]+".csv"  
        #= "./sp500_sectors"
        
        df_sectorList   = df.loc[ (df['GICS Sector'] == df_array[i])]    
        df_Sector       = pd.DataFrame(columns = ['Date'] )        
        df_Sector.set_index('Date', inplace = True)        
        
        for ticker in df_sectorList['Symbol']:          
            # get the moving average
            sourceFillpath = const.sp500dataWorkingDir_const + "/" + ticker + ".csv"
            newCol_dayMA = str(maDay_int) + "MA" 
            
            df_ticker = getDateFrame.getDataFrame_tick(sourceFillpath, ticker)
            if not df_ticker.empty:
                df_ticker[newCol_dayMA]     = df_ticker['Close'].rolling(window = maDay_int).mean()
                df_ticker['%Close/MA']  = (df_ticker['Close'] / df_ticker[newCol_dayMA])*100
                # df_ticker[ticker] = floor(df_ticker['Close'] / df_ticker[newCol_dayMA])
                df_ticker[ticker]       = floor(df_ticker['Close'] / df_ticker[newCol_dayMA])
                
                # add the col MA 0 or 1 to the sector file
                df_Sector = pd.DataFrame.join(df_Sector, df_ticker[ticker], how='outer')
                                # ---for testing
                if logOn:                    
                    tempFilePath = const.sp500_sectorsDir_tempConst + "/" + ticker+".csv"
                    df_ticker.to_csv(tempFilePath, index='Date', float_format='% .0f')
                                #--------------
            else:
                print("\nNo stock data available calSP500Sector. "+ sourceFillpath)
        
        array_TotalCount = (df_Sector.agg("sum", axis="columns"))
        int_totalNumOfStock = len(df_sectorList['Symbol'])
        # df_temp['TotalCount'] = (df_Sector.agg("sum", axis="columns")) 
        # df_temp['TotalNumOfStock'] = len(df_sectorList['Symbol'])
        
        name_sectorMA_Mean = df_array[i]
        # df_Sector[name_sectorMA_Mean] = (df_Sector.agg("mean", axis="columns"))*100 
        # array_sectorMA_Mean = (df_Sector.agg("mean", axis="columns"))*100
        
        # df_Sector.insert(len(df_sectorList['Symbol']), 'TotalCount', array_TotalCount, True) 
        # df_Sector.insert(len(df_sectorList['Symbol']), 'TotalNumOfStock', int_totalNumOfStock, True)

        
        df_Sector['TotalCount'] = array_TotalCount
        df_Sector['TotalNumOfStock'] = int_totalNumOfStock
        
        df_Sector[name_sectorMA_Mean] = df_Sector['TotalCount']/df_Sector['TotalNumOfStock'] *100
        # df_Sector[name_sectorMA_Mean] = array_sectorMA_Mean
        
        
        df_Sector.to_csv(sectorFilePath, index='Date', float_format='% .0f')        
        # print("")
        
import seaborn as sb
import matplotlib.pyplot as plt
def updateMarketBreadth_SP500Sector(maDay_int):    
    """
    Update market breath
    Input:
        maDay: int
    """
    
    marketBreadthFilePath = const.sp500_sectorsDir_marketBreadthConst + "/" + str(maDay_int) +"MA.csv"
    df_MarketBreadth = pd.DataFrame(columns = ['Date'] ) 
    df_MarketBreadth.set_index('Date', inplace = True)
    # sourcePath = const.sp500_sectors 
    
    files = glob.glob(const.sp500_sectorsDir_const + "/*.csv")    
    
    df_temp = pd.DataFrame(columns = ['Date', 'TotalCount', 'TotalNumOfStock', 'Temp'] ) 
    df_temp.set_index('Date', inplace = True)
    for f in files:
        pd_csv = pd.read_csv(f, index_col='Date')

        df_temp['Temp']  = pd_csv['TotalCount']                
        df_temp['TotalCount']  = df_temp['Temp'] + df_temp['TotalCount'].fillna(0) 
        
        df_temp['Temp']  = pd_csv['TotalNumOfStock']                
        df_temp['TotalNumOfStock']  = df_temp['Temp'] + df_temp['TotalNumOfStock'].fillna(0) 

        
        # # df[df.columns[-1]]  df.iloc[:,-1:]  pd_csv.iloc[:,-1:]      
        df_MarketBreadth = pd.DataFrame.join(df_MarketBreadth, pd_csv[pd_csv.columns[-1]], how='outer')
    

    # df_MarketBreadth.insert(0, 'Total', df_MarketBreadth.agg("sum", axis="columns"), True) 
    # df_MarketBreadth['Total'] = (df_MarketBreadth.agg("sum", axis="columns"))    
    # df_MarketBreadth.insert(0, 'SP500Cal', (df_temp['TotalCount']/df_temp['TotalNumOfStock'])*100 , True)
      
    df_temp['Temp'] = (df_MarketBreadth.agg("sum", axis="columns")) 
    
    # df_MarketBreadth['SP500Cal'] = (df_temp['TotalCount']/df_temp['TotalNumOfStock'])*100
    df_MarketBreadth.insert(0, 'SP500Cal', (df_temp['TotalCount']/df_temp['TotalNumOfStock'])*100 , True)
    
    df_MarketBreadth['Total'] = df_temp['Temp'] 

    df_MarketBreadth.sort_values('Date', ascending=False, inplace=True)
    
    df_MarketBreadth.to_csv(marketBreadthFilePath, index='Date', float_format='% .0f')  
    # print('')

# TODO delete this section
# #-----------
#     marketBreadthFilePath = "./sp500_sectors/market_breadth/20MA.csv"
#     df_MarketBreadth = pd.read_csv(marketBreadthFilePath, index_col='Date')
    
#     df_MarketBreadth1 = df_MarketBreadth.iloc[0:10, :-1]
#     # df_MarketBreadth1 = (df_MarketBreadth.iloc[0:100, :-1]).to_numpy()
    
#     # cmap=sb.diverging_palette(20,145, s=60, as_cmap=True)
#     print("")
#     # # heatM = sb.heatmap(df_MarketBreadth, cmap=cmap, annot=True, annot_kws={"size": 6.5}, fmt=".1%",center=0, linewidths=.1)
    
#     # heatM = sb.heatmap(df_MarketBreadth)
#     # sb.heatmap(df_MarketBreadth1)
    
    
#     fig, ax = plt.subplots(figsize=(14,6))
    
#     plt.title('S&P 500 Market Breadth 20 MA Heat Map',fontsize=18)
#     ax.title.set_position([0.5,0.1]) #ax.title.set_position([0.5,1.05])
    
#     # ax.set_xticks([])
#     sb.heatmap(df_MarketBreadth1, annot=True, fmt="", cmap='RdYlGn', ax=ax)#

    
    
#     plt.show()
#     # heatM.figure.savefig("sectoral.png", dpi=800)

    
# #----------------------------------------------
# # sourceFillpath = "test1.csv"

# # df = pd.read_csv(sourceFillpath, parse_dates=['Date'], index_col='Date') 
# # print (df1)

# # calMA_SP500Sector(maDay_int = 20, logOn = False)

# updateMarketBreadth_SP500Sector(maDay_int=20)


  





#         # core.window.Rolling
#         # core.window.ExponentialMovingWindow     
# # >>> xlsx = pd.ExcelFile('file.xls')
# # >>> df = pd.read_excel(xlsx,  'Sheet1')        