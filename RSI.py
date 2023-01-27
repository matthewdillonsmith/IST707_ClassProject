# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 18:55:11 2021

@author: sinti
"""

#Import OHLCV data and calculate RSI technical indicators
# Author : Mayank Rasu

# Please report bug/issues in the Q&A section
# =============================================================================

# Import necesary libraries
import pandas as pd
import yfinance as yf
import numpy as np
import datetime as dt

# Download historical data for required stocks
ticker = "AAPL"
ohlcv = yf.download(ticker,dt.date.today()-dt.timedelta(1825),dt.datetime.today())

df = ohlcv.copy()

def RSI(DF,n):
    "function to calculate RSI"
    df = DF.copy()
    df['delta']=df['Adj Close'] - df['Adj Close'].shift(1) #daily change in close price
    df['gain']=np.where(df['delta']>=0,df['delta'],0)# np is a conditional step "if first condition then the next "
    df['loss']=np.where(df['delta']<0,abs(df['delta']),0)
    avg_gain = [] # loops over the data
    avg_loss = []
    gain = df['gain'].tolist() # converted to a list
    loss = df['loss'].tolist()
    for i in range(len(df)): # loops over the entire data range
        if i < n:
            avg_gain.append(np.NaN)
            avg_loss.append(np.NaN)
        elif i == n:
            avg_gain.append(df['gain'].rolling(n).mean().tolist()[n])
            avg_loss.append(df['loss'].rolling(n).mean().tolist()[n])
        elif i > n:
            avg_gain.append(((n-1)*avg_gain[i-1] + gain[i])/n)
            avg_loss.append(((n-1)*avg_loss[i-1] + loss[i])/n)
    df['avg_gain']=np.array(avg_gain)#np.array converts lits to arrays
    df['avg_loss']=np.array(avg_loss)
    df['RS'] = df['avg_gain']/df['avg_loss']
    df['RSI'] = 100 - (100/(1+df['RS']))
    return df['RSI']


RSI(ohlcv,14)
