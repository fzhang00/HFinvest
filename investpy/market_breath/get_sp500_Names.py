# -*- coding: utf-8 -*-
"""

"""
import pandas as pd
import os.path as myPath
from datetime import date, datetime
# import os

##########constant

todayDate_str = datetime.today().strftime('%Y-%m-%d') 
now_str = str(datetime.now())
errorTxtfileName_const = todayDate_str + ' errorlog.txt'
# todayDateOffset_str = ( datetime.today() + timedelta(days=-720) ).strftime('%Y-%m-%d')  

errorTxtfileName_const = todayDate_str + ' errorlog.txt'

sp500dataWorkingDir_const = "./sp500_data"
sp500Info_file_const = "SP500-info.csv"
# sp500dataPrepDir_const    = "./sp500_prepData"

sp500_sectorsDir_const = "./sp500_sectors"


#------------------------------


oldSP500_file_const = todayDate_str +"_"+ sp500Info_file_const
tempfile_const = "SP500-infoTemp.csv"


#------------------------------
def createEmpty_sp500SectorsFiles(destDir):
    df      = pd.read_csv(sp500Info_file_const)
    df_array = df['GICS Sector'].unique()
    
    for i in range(len(df_array)):
        print(df_array[i]) 
        newFilePath = destDir + "/" + df_array[i]+".csv"  
        #= "./sp500_sectors"
        df4 = df.loc[ (df['GICS Sector'] == df_array[i])]
        
        # print (df4['Symbol'] )             
        # if  df['GICS Sector'] == df_array[i]:
        # df2 = pd.DataFrame(columns= df4['Symbol'] )  
        
        df2 = pd.DataFrame(columns = ['Date'] ) 
        df3 = pd.DataFrame(columns= df4['Symbol'] ) 
        df2 = pd.DataFrame.join(df2, df3, how='outer')
        df2.set_index('Date', inplace = True)
        # print (df2)
        df2.to_csv(newFilePath )
            
# createEmpty_sp500SectorsFiles(sp500_sectorsDir_const )
        
    # df.set_index(['GICS Sector', 'GICS Sub-Industry', 'Symbol'], inplace = True)
    # df.set_index(['GICS Sector', 'GICS Sub-Industry'], inplace = True)
    # df.set_index(['GICS Sector', 'GICS Sub-Industry'])
    # df = df.set_index('Symbol', inplace=True)
    
    #--------------------working
    # df1 = df['Symbol']
    # df1.to_csv("sp500sectorDetail.csv")
    
    # df2 = pd.read_csv("sp500sectorDetail.csv")
    # print (df2)
    # df1=df2.T
    # df1.to_csv("sp500sectorDetail_2.csv")
    #-----------------------------------
    
    # df1 = df['GICS Sector', 'GICS Sub-Industry', 'Symbol']

# table=pd.read_html('https://www.gurufocus.com/sector_shiller_pe.php')
# print("")

# https://www.lme.com/Metals/Non-ferrous#tabIndex=0
# table=pd.read_html('https://www.lme.com/Metals/Non-ferrous#tabIndex=0')
# table=pd.read_html('https://www.lme.com/Metals/Non-ferrous#060d7ad1-4aa2-4dca-8999-accdb19e581f-tab-0')

# df = table[0]
# print(df)



def update_sp500companyList():    
    table=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    df = table[0]
    df = df.sort_values(['GICS Sector', 'GICS Sub-Industry','Symbol'])
    
    if myPath.isfile(sp500Info_file_const): #file exist     
        df.to_csv(tempfile_const)
        dftemp = pd.read_csv(tempfile_const)
        df_currentCSV = pd.read_csv(sp500Info_file_const)
        
        # check if there is a new sp 500 stock; only with the same length.    
        try:
            newStock = df_currentCSV.compare(dftemp)        
        except Exception as ex:
            # print('Error:', ex)        
            if myPath.exists(errorTxtfileName_const):
                append_write = 'a' # append if already exists
            else:
                append_write = 'w' # make a new file if not        
            f = open(errorTxtfileName_const, append_write)
            f.write('\n'+now_str +'  compare SP500name exceptional - %s' % ex)# + str(ex) )#+ " "+tickers)
            f.close()    
        
        if newStock.empty:
            print ("S&P 500 no update")
            #no new stock updated do nothing 
        else:
            dftemp.to_csv(oldSP500_file_const)
            df.to_csv(sp500Info_file_const)
            newStock.to_csv(todayDate_str + ' newStock.csv')    
    else:
        df.to_csv(sp500Info_file_const)        





# dftemp = dftemp.append(df)['Symbol'].drop_duplicates()

# d={}
# d = dftemp.append(df)['Symbol'].unique()

    




# df2.loc[0, "col1"] = "c"
# len(df.columns)


# import pandas
# colnames = ['year', 'name', 'city', 'latitude', 'longitude']
# data = pandas.read_csv('test.csv', names=colnames)
# If you want your lists as in the question, you can now do:

# names = data.name.tolist()


# #print (table[0])

 #   Column                 Non-Null Count  Dtype 
# ---  ------                 --------------  ----- 
#  0   Symbol                 505 non-null    object
#  1   Security               505 non-null    object
#  2   SEC filings            505 non-null    object
#  3   GICS Sector            505 non-null    object
#  4   GICS Sub-Industry      505 non-null    object
#  5   Headquarters Location  505 non-null    object
#  6   Date first added       453 non-null    object
#  7   CIK                    505 non-null    int64 
#  8   Founded                505 non-null    object

# array(['Communication Services', 'Consumer Discretionary',
#        'Consumer Staples', 'Energy', 'Financials', 'Health Care',
#        'Industrials', 'Information Technology', 'Materials',
#        'Real Estate', 'Utilities'], dtype=object)