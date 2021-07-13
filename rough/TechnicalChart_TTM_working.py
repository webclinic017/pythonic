import datetime as dt
import random as rnd
from datetime import date, datetime, time, timedelta

import matplotlib.pyplot as plt
import mplfinance as mpf
import numpy as np
import pandas as pd
import pandas_ta as ta
import yfinance as yf
import plotly.graph_objects as go
import os


symbol = 'AAPL'
sd = datetime(2020, 1, 1)
ed = datetime(2021, 4, 7)

# df = yf.download(tickers=symbol, start=sd, end=ed, interval="60m")

# symbol = 'AAPL'
# sd = datetime(2020, 1, 1)
# ed = datetime(2021, 4, 7)
# dfdata = yf.download(tickers=symbol, start=sd, end=ed, interval="60m")
# dfdata.to_pickle(symbol+'.pickle')
# dfdata.to_pickle(symbol+'.pickle')
# dfdata = pd.read_csv('h:/WorkSpace_Python/AppPy/rough/'+symbol+'.csv', index_col='Datetime', parse_dates=True)
if os.name == 'nt': df = pd.read_pickle('h:/WorkSpace_Python/pythonic/rough/'+symbol+'.pickle')
else: df = pd.read_pickle('/home/towshif/code/python/pythonic/rough/'+symbol+'.pickle')

# df = yf.download(tickers=symbol, start=sd, end=ed, interval="1d")
# df = yf.download(tickers=symbol, start=sd, end=ed, interval="60m", prepost=True)
# df = yf.download(tickers=symbol, start=sd, end=ed, interval="30m")
# df = yf.download(tickers=symbol, start=sd, end=ed, interval="15m")
# df = yf.download(tickers=symbol, start=sd, end=ed, interval="5m")
# df = yf.download(tickers=symbol, start=sd, end=ed, interval="5m", prepost=True)
# df = yf.download(tickers=symbol, start=sd, end=ed, interval="15m", prepost=True)


# Lets start with a simple chart 
mpfdf = df.tail(100)

############     SIMPLE CANDLE CHART w/ volume 
# style = 'yahoo','nightclouds','ibd'
# type =  'candle', 'hollow_and_filled'
# mpf.plot(mpfdf, style='yahoo', type='candle', volume=True, panel_ratios=(4,1))


############    ADD some INDICATORS 
# squeezes = df.ta.squeeze(lazybear=False, detailed=True, append=True)
squeezes = df.ta.squeeze(lazybear=True, detailed=True, append=True)

bollingers = df.ta.bbands(append=True) # 'BBL_5_2.0', 'BBM_5_2.0', 'BBU_5_2.0', 'BBB_5_2.0' 
macd = df.ta.macd(append=True) # 'MACD_12_26_9', 'MACDh_12_26_9','MACDs_12_26_9'],
rsi = df.ta.rsi(length=20, append=True)
rsi_SMA = df['RSI_20_SMA'] = ta.sma(rsi, length=20, append=True)

rsx = df.ta.rsx(length=20, append=True)
rsx_SMA = df['RSX_20_SMA'] = ta.sma(rsx, length=20, append=True)


ema20 = df.ta.ema(length=20, append=True)
ema50 = df.ta.ema(length=50, append=True)
ema100 = df.ta.ema(length=100, append=True)
ema150 = df.ta.ema(length=150, append=True)
keltner = df.ta.kc(append=True)

def in_squeeze(df):
    if df['BBU_5_2.0'] > df['KCLe_20_2'] and df['BBL_5_2.0'] < df['KCLe_20_2'] : 
        return 0 
def out_squeeze(df):
    if not ( df['BBU_5_2.0'] > df['KCLe_20_2'] and df['BBL_5_2.0'] < df['KCLe_20_2']):         
        return 0
    
df['squeeze_on'] = df.apply(in_squeeze, axis=1)
df['squeeze_off'] = df.apply(out_squeeze, axis=1)


mpfdf_columns = list(df.columns)


############    PLOT TTM SQUEEZE 


# taplots = [] 
# taplots += 
mpfdf = df.tail(150)
apsq = [
        # make same as TOS colors 
        mpf.make_addplot(mpfdf[squeezes.columns[-3]], type="bar", color="blue", alpha=0.65, panel=1),
        mpf.make_addplot(mpfdf[squeezes.columns[-4]], type="bar", color="deepskyblue", alpha=0.65, panel=1),
        mpf.make_addplot(mpfdf[squeezes.columns[-2]], type="bar", color="red", alpha=0.65, panel=1),
        mpf.make_addplot(mpfdf[squeezes.columns[-1]], type="bar", color="yellow", alpha=0.65, panel=1),
        # mpf.make_addplot(mpfdf['close'], color="black", panel=1),
        mpf.make_addplot(mpfdf[squeezes.columns[4]], ylabel="TTM Squeeze", color="green", panel=1),
        mpf.make_addplot(mpfdf[squeezes.columns[5]], color="red",  panel=1),
        # squeeze metrics 
        mpf.make_addplot(mpfdf[squeezes.columns[1]], scatter=True,markersize=10,marker='o', color="red",  panel=2),
        mpf.make_addplot(mpfdf[squeezes.columns[2]], scatter=True,markersize=15,marker='o',color="green",  panel=2),
        mpf.make_addplot(mpfdf[squeezes.columns[3]], scatter=True,markersize=20,marker='o',color="skyblue",  panel=2),

        mpf.make_addplot(mpfdf['squeeze_on'], scatter=True,markersize=10,marker='o', color="black",  panel=1),
        mpf.make_addplot(mpfdf['squeeze_off'], scatter=True,markersize=10,marker='o', color="lime",  panel=1),        
        ]
# mpfchart["plot_ratios"] += common_plot_ratio # Required to add a new Panel

mpf.plot(mpfdf,type='candle', addplot=apsq, figscale=1.1, figratio=(8,5),title= symbol+'\nTTM-Squeeze', style='yahoo',volume=False,panel_ratios=(6,2,2))

