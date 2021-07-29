import sys
sys.path.append("../fan_lib")
import datetime
from functools import reduce
import pandas as pd
import numpy as np
import holoviews as hv
import pandas_datareader as web
from invest_db import InvestDB, FAN_SQL, RYAN_SQL, QUANDL_KEY

_START_DATE = datetime.datetime(1970,1,1)
_END_DATE = datetime.datetime.today()
_TODAY = datetime.datetime.today()

def sp500_market_breadth_prep():
    from ..market_breadth import sp500Const as spconst
    mb_dir = spconst.sp500_sectorsDir_marketBreadthConst
    mb_df = pd.read_csv(mb_dir+"/20MA.csv", parse_dates=[0])
    sp500 = web.DataReader('^GSPC', 'yahoo', mb_df['Date'].min(), mb_df['Date'].max())#， api_key=QUANDL_KEY)
    sp500.reset_index(inplace=True)

def compute_change_percentage(df, column):
    """Compute the percentage change of last record for column"""
    s = df[column].dropna()
    try:
        return (s.iloc[-1]-s.iloc[-2])/s.iloc[-2]*100
    except IndexError:
        return 0

def compute_change(df, column):
    """Compute the percentage change of last record for column"""
    s = df[column].dropna()
    return (s.iloc[-1]-s.iloc[-2])

def normalize_column(df, column):
    """Normalize a Dataframe column by its std()"""
    s_std = df[column].dropna().std()
    return df[column]/s_std

def prep_fed_db_data(db, symbols, 
                    start_date=_START_DATE, 
                    end_date=_END_DATE):
    """Returns a dataframe of FRED data extracted from FED database"""
    symbol_df = db.get_filtered_data('FED_US_SYMBOL', 
                                    ['Symbol', 'Description', 'Category'], 
                                    with_date=False)
    symbol_tb = symbol_df.loc[symbol_df['Symbol'].isin(symbols)]
    symbol_to_download = pd.DataFrame([{'Symbol':s, 'Description':None, 'Category':None }\
                                         for s in symbols if s not in list(symbol_df['Symbol'])])
    print(",".join(list(symbol_to_download['Symbol'])), "is not in database")
    # get distinct Category to construct table
    unique_category = symbol_tb['Category'].unique()
    dfs = []
    for c in unique_category:
        table_name = 'FED_'+'_'.join(c.upper().split(' '))
        dfs.append(db.get_filtered_data(table_name, 
                                        list(symbol_tb['Symbol'].loc[symbol_tb['Category']==c])
                                        ))
    try:
        dfs.append(web.DataReader(symbol_to_download['Symbol'],'fred', start_date, end_date))
        symbol_tb = pd.concat([symbol_tb, symbol_to_download])
    except web._utils.RemoteDataError:
        print("One of your symbol {} not exists on FRED server.".format(list(symbol_to_download['Symbol'])))
    output= reduce(lambda  left,right: pd.merge(left,right,on=['DATE'], how='outer'), dfs)
    output.reset_index(inplace=True)
    output.rename(columns={'index':'Date'}, inplace=True)
    return output, symbol_tb

def prep_yahoo_multi_data(symbol_list, column='Adj Close', 
                         start_date=_START_DATE, end_date=_END_DATE):
    """Return a dataframe for data from Yahoo on multiple symbol on specific column"""
    data = web.DataReader(symbol_list, 'stooq', start_date, end_date, api_key=None)
    #combined=commodity.loc[:, [('Date', ''),('Adj Close','GC=F'), ('Adj Close', 'CL=F'),('Adj Close', 'HG=F')]]
    output = data.loc[:, [(column, s) for s in symbol_list]]
    output.columns = [' '.join(col).strip() for col in output.columns.values]
    symbol_tb=pd.DataFrame({'Symbol':output.columns})
    output.reset_index(inplace=True)
    output.rename(columns={'Date':'DATE'}, inplace=True)
    return output, symbol_tb

def prep_sp500_index(start_date=datetime.datetime(2000,1,1), 
                    end_date=datetime.datetime.today()):
    """Returns a dataframe with SP500 INDEX"""
    return web.DataReader('^GSPC', 'yahoo', start_date, end_date)



def add_sma(df, columns, n):
    for c in columns:
        df[c+'_sma'] = df[c].rolling(n).mean()
    return df

def create_curves(df, x, columns=None, ylabel="", group=None):
    """
    Return a list with hvCurve objects.
    """
    if columns is None:
        columns = list(df.columns)
        columns.remove(x) # remove the x axis

    changes = {c:compute_change_percentage(df, c) for c in columns}

    df.fillna(method='ffill', inplace=True)
    curves = hv.Overlay([hv.Curve(df, x, (column, ' '.join([ylabel, column])), 
                                  label=','.join([column, 
                                                 "{:.2f}%".format(changes[column]),
                                                 "{:.2e}".format(df[column].iloc[-1])])) \
                         for column in columns], group=group)
    return curves
        
    
def create_normalized_curves(df, x, columns, changes=None,  ylabel="", group=None):
    """
    Return a list of normalized hv.Curve objects.
    Input:
        df: a pandas dataframe
        columns: a list of columns to plot
    """
    if changes is None:
        curves = hv.Overlay([hv.Curve((df[x], normalize_column(df, column)), label=column+'_normalized')
                for column in columns])
    else:
        curves = hv.Overlay([hv.Curve((df[x], normalize_column(df, column)), kdims=['Date'], label=','.join([column, "{:.2f}%".format(changes[column])])) for column in columns])
    return curves

def prep_commodity_stock(db, view, sma_w):
    stock = db.get_filtered_data(view, ['Stock', 'Exchange'])
    stock = stock.reset_index()
    stock_w = (stock.groupby(['Exchange', pd.Grouper(freq='W', key='DATE')])['Stock'].mean()).to_frame().reset_index()
    stock_w.sort_values(by=['DATE'], inplace=True)
    wstock_pivot = stock_w.pivot(index='DATE', columns='Exchange')['Stock'].reset_index()
    wstock_pivot.columns.name = None
    wstock_pivot.fillna(0, inplace=True)
    wstock_pivot['Total'] = wstock_pivot['COMEX']+wstock_pivot['LME']+wstock_pivot['SHFE']
    stockw_sma = add_sma(wstock_pivot, ['Total', 'LME', 'COMEX', 'SHFE'], sma_w)
    return stock, stock_w, stockw_sma

def create_commodity_stock_overlay(stocks, group):
    stock_tab = pd.melt(stocks, id_vars=['DATE'], var_name='Exchange', value_name='Stock')
    stockTable = hv.Table(stock_tab, ['DATE', 'Exchange'], 'Stock')
    stock_bar = hv.Bars(stockTable, group=group)
    lme_sma = hv.Curve(stocks, 'DATE', 'LME_sma')
    cmx_sma = hv.Curve(stocks, 'DATE', 'COMEX_sma')
    shfe_sma = hv.Curve(stocks, 'DATE', 'SHFE_sma')
    totl_sma = hv.Curve(stocks, 'DATE', 'Total_sma')
    return stock_bar*lme_sma*cmx_sma*shfe_sma*totl_sma

def create_long_short_grid(future, forward_month, dat):
    dat_filtered = dat[dat['Future'].str.strip()==future]
    dat_filtered = dat_filtered[ dat_filtered['ForwardMonth']==forward_month]
    l_curve = hv.Curve(dat_filtered, 'DATE', 'Long Qty', label='Long')
    s_curve = hv.Curve(dat_filtered, 'DATE', 'Short Qty', label='Short')
    return l_curve*s_curve

class CommodityCharts():
    # Tables and Views of Commodity Database
    _DATABASE = "Commodity_A1"
    _CU_STOCK_VIEW = "STOCK_COPPER"
    _AL_STOCK_VIEW = "STOCK_ALUMINUM"
    _BASE_METAL_PRICE_LME_TABLE = "LME_baseMetal_price"
    _PREC_METAL_PRICE_LME_TABLE = "LME_precious_price"
    _LME_FUTURE_PRICE_VOL = {'Copper': {'price':'Copper', 'volume':'Copper Future'},
                            'Aluminium': {'price':'Aluminium', 'volume':'Primary Aluminium Future'}}

    def __init__(self, db_info, width=900, height=300):
        db_info['database']=self._DATABASE
        self.db = InvestDB(db_info)
        self.chart_width=width
        self.chart_height=height

    def get_basemetal_future_pv_lme(self, metal):
        # get price
        price = self.db.get_filtered_data('LME_baseMetal_price', 
                                        ['CashBuyer', 'Month3_Buyer', 'Month15_Buyer', 'Dec1_Buyer'],
                                        column_to_match='Contract', 
                                        value_to_match=self._LME_FUTURE_PRICE_VOL[metal]['price'])
        price = price.dropna(axis=1, how='all')
        price.reset_index(inplace=True)
        # get volume
        volume = self.db.get_filtered_data('LME_Daily_Volume', ['Volume'],
                                           column_to_match='Description', 
                                           value_to_match=self._LME_FUTURE_PRICE_VOL[metal]['volume'])
        volume.reset_index(inplace=True)
        return price, volume    

    def get_cu_future_price_volume_lme(self):
        self.cu_price_lme, self.cu_volume_lme = self.get_basemetal_future_pv_lme('Copper')

    def get_al_future_price_volume_lme(self):
        self.al_price_lme, self.al_volume_lme = self.get_basemetal_future_pv_lme('Aluminium')    

    def get_basemetal_stock_global(self, table, sma_d, sma_w):
        stock = self.db.get_filtered_data(table, ['Stock', 'Exchange'])
        stock = stock.reset_index()
        stock_pivot = stock.pivot(index='DATE', columns='Exchange')['Stock'].sort_values('DATE').reset_index()
        stock_pivot.columns.name = None
        stock_pivot = add_sma(stock_pivot, ['LME', 'COMEX', 'SHFE'], sma_d)
        stock_w = (stock.groupby(['Exchange', pd.Grouper(freq='W', key='DATE')])['Stock'].mean()).to_frame().reset_index()
        stock_w.sort_values(by=['DATE'], inplace=True)
        wstock_pivot = stock_w.pivot(index='DATE', columns='Exchange')['Stock'].reset_index()
        wstock_pivot.columns.name = None
        wstock_pivot.sort_values('DATE', inplace=True)
        wstock_pivot.fillna(0, inplace=True)
        wstock_pivot['Total'] = wstock_pivot['COMEX']+wstock_pivot['LME']+wstock_pivot['SHFE']
        wstock_pivot = add_sma(wstock_pivot, ['Total', 'LME', 'COMEX', 'SHFE'], sma_w)
        return stock_pivot, wstock_pivot

    def get_cu_stock_global(self, sma_d=10, sma_w=10):
        self.cu_stock, self.cu_stock_weekly = self.get_basemetal_stock_global(self._CU_STOCK_VIEW, sma_d, sma_w)

    def get_al_stock_global(self, sma_d=10, sma_w=10):
        self.al_stock, self.al_stock_weekly = self.get_basemetal_stock_global(self._AL_STOCK_VIEW, sma_d, sma_w)
        
    def make_copper_stock_chart(self, sma_d=10, sma_w=10):
        # populate self.cu_stock, self.cu_stock_weekly
        self.get_cu_stock_global(sma_d, sma_w)
        self.cu_stock_overlay = create_commodity_stock_overlay(self.cu_stock_weekly, 'Copper Weekly Stock and SMA')

    def make_aluminium_stock_chart(self, sma_d=10, sma_w=10):
        self.get_al_stock_global(sma_d, sma_w)
        self.al_stock_overlay = create_commodity_stock_overlay(self.al_stock_weekly, 'Aluminium Weekly Stock and SMA')

    def make_comex_longshort_gridplot(self, futures):
        ls_dat = self.db.get_filtered_data('COMEX_Daily_Report_OpenInterest_LongShortPositon', ['[Future]', '[ForwardMonth]','[Long Qty]', '[Short Qty]'])
        ls_dat['Future']=ls_dat['Future'].str.strip()
        ls_dat.sort_values('DATE', inplace=True)
        # https://stackoverflow.com/questions/13611065/efficient-way-to-apply-multiple-filters-to-pandas-dataframe-or-series
        ls_filt = ls_dat.query('|'.join([f'Future=="{f}"' for f in futures]))
        f_months = pd.unique(ls_filt['ForwardMonth'])
        f_months.sort()
        f_months = f_months[f_months>(np.datetime64(_TODAY- datetime.timedelta(days=180)))]
        curve_dict = {(fmonth, future):create_long_short_grid(future, fmonth, ls_filt)
                      for future in futures
                      for fmonth in f_months[0:7]}
        return curve_dict

def test():
    db = InvestDB(FAN_SQL)    
    employ_symbols = ['ICSA', 'CCSA', 'JTSJOL', 'JTSHIL','JTSTSL', 'JTSQUL', 'JTSLDL']
    employ_df, employ_changes, symbol_tb= prep_fed_db_data(db, employ_symbols)
    print(employ_df.head(3))
    print(employ_changes)
    print(symbol_tb)

if __name__=="__main__":
    test()