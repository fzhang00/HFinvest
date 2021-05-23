# -*- coding: utf-8 -*-
"""
Created on Sun May  2 12:48:47 2021

@author: haoli
"""

def sql_load_csvFile_goldSilver_Vol_OI(fileFullPath):
    _server = 'RyanPC'
    _database = 'Commodity_A1' 
    _username = 'hl' 
    _password = '123' 
    
    _sqlTable_LME_baseMetal_stock = 'LME_baseMetal_stock'
    _sqlTable_LME_baseMetal_price = 'LME_baseMetal_price'
    _sqlTable_LME_precious_price = 'LME_precious_price'
    _sqlTable_LME_precious_VolOpenInterest = 'LME_precious_VolOpenInterest'

    df = pd.read_csv(fileFullPath)
    df_Vol_OI = df.replace({np.NAN: None}) 
    # whitespace_remover(df_Vol_OI)
    
    convertDateByColNum = 0
    date_fromFolderName = '2021-05-02'
    df_Vol_OI_updated = convertDDMM_date(df_Vol_OI, date_fromFolderName, convertDateByColNum)    
    df_Vol_OI_updated =  df_Vol_OI_updated.sort_values(df_Vol_OI_updated.columns[convertDateByColNum])
    
    savePath = constA.getFilePathInfo(fileFullPath, 0) #/temp/2021-04-01
    df_Vol_OI_updated.to_csv(savePath + '/updated_file.csv')
    
    
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server+';DATABASE='+_database+';UID='+_username+';PWD='+_password)
    cursor = cnxn.cursor()   
    
    for index, row in df_Vol_OI_updated.iterrows(): #: #dfvolOI.iterrows():   
        # print (row)
        # row
        query = """DELETE FROM %s where Date = '%s' and [Future] = '%s' ;""" %  (_sqlTable_LME_precious_VolOpenInterest, row[0], row[1])
        cursor.execute(query)
        query = """INSERT INTO %s ([Date], [Future], [Volume], [OpenInterest]) VALUES (?,?,?,?);"""  %(_sqlTable_LME_precious_VolOpenInterest)
        params = (row[0], row[1], row[2], row[3] )
        cursor.execute(query, params)              
    cnxn.commit()
    cursor.close()
    cnxn.close()
    print()    
    
fileFullPath= constLME_a.commodityLME_workDir_A + '/workFolder/LME Gold and silver 2021-01 02 03 Open Interest and Volumes.csv'
sql_load_csvFile_goldSilver_Vol_OI(fileFullPath)
print()


def sql_load_csvFile_baseMetal_price(fileFullPath):
    _server = 'RyanPC'
    _database = 'Commodity_A1' 
    _username = 'hl' 
    _password = '123' 
    
    _sqlTable_LME_baseMetal_stock = 'LME_baseMetal_stock'
    _sqlTable_LME_baseMetal_price = 'LME_baseMetal_price'
    _sqlTable_LME_precious_price = 'LME_precious_price'
    _sqlTable_LME_precious_VolOpenInterest = 'LME_precious_VolOpenInterest'
     

    df = pd.read_csv(fileFullPath)
    # df_Vol_OI = df.replace({np.NAN: None}) 
    df_price = df.replace({np.NAN: None})
    
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server+';DATABASE='+_database+';UID='+_username+';PWD='+_password)
    cursor = cnxn.cursor()    
    
     #----------table 1 ---
    for index, row in df_price.iterrows(): #: #dfvolOI.iterrows():   
        query = """DELETE FROM %s where Date = '%s' and [Contract] = '%s' ;""" % (_sqlTable_LME_baseMetal_price, row[0], row[1])
        cursor.execute(query)   
        
        query = """INSERT INTO %s VALUES (?,?,?,?, ?,?,?,?, ?,? );""" %(_sqlTable_LME_baseMetal_price)           
        params = (tuple(row) )
        # print(params)
        cursor.execute(query, params)              
    cnxn.commit()
    cursor.close()
    cnxn.close()    
 
    
fileFullPath= constLME_a.commodityLME_workDir_A + '/workFolder/LME_basemetal_sum_price.csv'
sql_load_csvFile_baseMetal_price(fileFullPath)
print()

def update_DateFormat(df):         
    for i in range(len(df)): 
        yy = datetime.strptime(df.iat[i, 0], '%d %b %Y').strftime('%Y-%m-%d')
        df.iat[i, 0] = yy
    print()
def sql_load_csvFile_baseMetal_Stock(fileFullPath):
    _server = 'RyanPC'
    _database = 'Commodity_A1' 
    _username = 'hl' 
    _password = '123' 
    
    _sqlTable_LME_baseMetal_stock = 'LME_baseMetal_stock'
    _sqlTable_LME_baseMetal_price = 'LME_baseMetal_price'
    _sqlTable_LME_precious_price = 'LME_precious_price'
    _sqlTable_LME_precious_VolOpenInterest = 'LME_precious_VolOpenInterest'
     

    df = pd.read_csv(fileFullPath)
    df_Stock = df.replace({np.NAN: None}) 
    # df_price = df.replace({np.NAN: None})
    
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server+';DATABASE='+_database+';UID='+_username+';PWD='+_password)
    cursor = cnxn.cursor()    

    for index, row in df_Stock.iterrows(): #: #dfvolOI.iterrows():   
        query = """DELETE FROM %s where Date = '%s' and [Future] = '%s' ;""" % (_sqlTable_LME_baseMetal_stock, row[0], row[1])
        cursor.execute(query)   
        
        query = """INSERT INTO %s VALUES (?,?,?,?,?);""" %(_sqlTable_LME_baseMetal_stock)           
        params = (tuple(row) )
        
        # print(params)
        cursor.execute(query, params)              
    cnxn.commit()
    cursor.close()
    cnxn.close()    
    print()     
    
fileFullPath= constLME_a.commodityLME_workDir_A + '/workFolder/LME_basemetal_sum_stock.csv'
sql_load_csvFile_baseMetal_Stock(fileFullPath)
print()

def sql_load_csvFile_baseMetal_Stock(fileFullPath):
    _server = 'RyanPC'
    _database = 'Commodity_A1' 
    _username = 'hl' 
    _password = '123' 
    
    _sqlTable_LME_baseMetal_stock = 'LME_baseMetal_stock'
    _sqlTable_LME_baseMetal_price = 'LME_baseMetal_price'
    _sqlTable_LME_precious_price = 'LME_precious_price'
    _sqlTable_LME_precious_VolOpenInterest = 'LME_precious_VolOpenInterest'     

    df = pd.read_csv(fileFullPath)
    df_Stock = df.replace({np.NAN: None}) 
    # df_price = df.replace({np.NAN: None})
    
    update_DateFormat(df_Stock)
    df_Stock = df_Stock.sort_values( df_Stock.columns[0])
    
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+_server+';DATABASE='+_database+';UID='+_username+';PWD='+_password)
    cursor = cnxn.cursor()    

    for index, row in df_Stock.iterrows(): #: #dfvolOI.iterrows():   
        query = """DELETE FROM %s where Date = '%s' and [Future] = '%s' ;""" % (_sqlTable_LME_baseMetal_stock, row[0], row[1])
        cursor.execute(query)   
        
        query = """INSERT INTO %s VALUES (?,?,?,?,?);""" %(_sqlTable_LME_baseMetal_stock)           
        params = (tuple(row) )
        
        print(params)
        cursor.execute(query, params)              
    cnxn.commit()
    cursor.close()
    cnxn.close()    
    print()     

    
fileFullPath= constLME_a.commodityLME_workDir_A + '/workFolder/basemetal Stocks 2020-2021-03.csv'
sql_load_csvFile_baseMetal_Stock(fileFullPath)
print()