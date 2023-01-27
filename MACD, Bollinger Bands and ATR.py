# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 17:09:27 2021

@author: sinti
"""

import pandas_datareader.data as pdr
import datetime

ticker = "MSFT"
ohlcv = pdr.get_data_yahoo(ticker,datetime.date.today() - datetime.timedelta(1825), datetime.date.today())
    


def MACD(DF,a,b,c):
    df = DF.copy()
    df['MA_Fast'] = df["Adj Close"].ewm(span=a,min_periods=a).mean()  
    df['MA_Slow'] = df["Adj Close"].ewm(span=b,min_periods=b).mean() 
    df["MACD"]=df["MA_Fast"]-df["MA_Slow"]   
    df['Signal']=["MACD"].ewm(span=c,min_periods=c).mean() 
    df.dropna(inplace=True)
    return df

def ATR(DF,n):
    df = DF.copy()
    df["H-L"]=abs(df['High']-df["Low"])
    df["H-PC"]=abs(df['High']-df["Adj Close"].shift(1))
    df["L-PC"]=abs(df['Low']-df["Adj Close"].shift(1))
    df['TR']= df[['H-L','H-PC','L-PC']].max(axis=1,skipna=False)
    df['ATR']= df['TR'].rolling(n).mean()
    
    df2 = df.drop(["H-L",'H-PC',"L-PC"],axis=1)
    return df2


def BollBnd(DF,n):
    df = DF.copy()
    df["MA"]=df["Adj Close"].rolling(n).mean()
    df["BB_up"] = df["MA"] + 2*df['MA'].rolling(n).std()
    df["BB_dn"] = df["MA"] - 2*df['MA'].rolling(n).std()
    df["BB_width"] = df["BB_up"] - df["BB_dn"]
    df.dropna(inplace=True)
    return df


BollBnd(ohlcv,20).iloc[-100:,[-4,-3,-2]].plot()
