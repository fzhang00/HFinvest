import pandas as pd
import numpy as np
import pandas_datareader as web


def sp500_market_breadth_prep():
    from ..market_breadth import sp500Const as spconst
    mb_dir = spconst.sp500_sectorsDir_marketBreadthConst
    mb_df = pd.read_csv(mb_dir+"/20MA.csv", parse_dates=[0])
    sp500 = web.DataReader('^GSPC', 'yahoo', mb_df['Date'].min(), mb_df['Date'].max())#， api_key=QUANDL_KEY)
    sp500.reset_index(inplace=True)

def compute_change_percentage(df, column):
    """Compute the percentage change of last record for column"""
    s = df[column].dropna()
    return (s.iloc[-1]-s.iloc[-2])/s.iloc[-2]*100

def compute_change(df, column):
    """Compute the percentage change of last record for column"""
    s = df[column].dropna()
    return (s.iloc[-1]-s.iloc[-2])

def normalize_column(df, column):
    """Normalize a Dataframe column by its std()"""
    s_std = df[column].dropna().std()
    return df[column]/s_std

