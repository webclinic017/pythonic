import datetime as dt
import os
import random as rnd
from datetime import date, datetime, time, timedelta

import matplotlib.pyplot as plt
import mplfinance as mpf
import numpy as np
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
import yfinance as yf



symbol = 'AAL'
sd = datetime(2020, 1, 1)
ed = datetime(2021, 4, 12)
interval = "1d"
# interval = "60m"

# df = yf.download(tickers=symbol, start=sd, end=ed, interval="60m")
# df = yf.download(tickers=symbol, start=sd, interval="60m")
# df = yf.download(tickers=symbol, start=sd, end=ed, interval="1d")
# dfd = yf.download(tickers=symbol, start=sd, interval=interval,prepost=True)
dfd = yf.download(tickers=symbol, start=sd, interval=interval)
df = dfd


# Enable if 4H reampling is True 
# dfd = yf.download(tickers=symbol, start=sd, interval=interval,prepost=True)
dfd = yf.download(tickers=symbol, start=sd, interval=interval)
df = dfd
interval = "4h"
# Resampling Code 
## Resample to 4H timefeame 
aggregation = {'Open'  :'first',
               'High'  :'max',
               'Low'   :'min',
               'Close' :'last',
               'Volume':'sum'}
df = dfd.resample('4H').agg(aggregation).dropna()

# symbol = 'AAPL'
# sd = datetime(2020, 1, 1)
# ed = datetime(2021, 4, 7)
# dfdata = yf.download(tickers=symbol, start=sd, end=ed, interval="60m")
# dfdata.to_pickle(symbol+'.pickle')
# dfdata.to_pickle(symbol+'.pickle')
# dfdata = pd.read_csv('h:/WorkSpace_Python/AppPy/rough/'+symbol+'.csv', index_col='Datetime', parse_dates=True)
# if os.name == 'nt': df = pd.read_pickle('h:/WorkSpace_Python/pythonic/rough/'+symbol+'.pickle')
# else: df = pd.read_pickle('/home/towshif/code/python/pythonic/rough/'+symbol+'.pickle')

# df = yf.download(tickers=symbol, start=sd, end=ed, interval="1d")
# df = yf.download(tickers=symbol, start=sd, end=ed, interval="60m", prepost=True)
# df = yf.download(tickers=symbol, start=sd, end=ed, interval="30m")
# df = yf.download(tickers=symbol, start=sd, end=ed, interval="15m")
# df = yf.download(tickers=symbol, start=sd, end=ed, interval="5m")
# df = yf.download(tickers=symbol, start=sd, end=ed, interval="5m", prepost=True)
# df = yf.download(tickers=symbol, start=sd, end=ed, interval="15m", prepost=True)




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

ha = df.ta.ha(append=True)
df['HA_color'] = np.where(df.HA_close > df.HA_open, 1, -1)
# ema21HA = df['EMA_21HA'] = ta.ema( df.HA_close, length=21, append=True)

ema21 = df.ta.ema(length=21, append=True)
ema50 = df.ta.ema(length=50, append=True)
ema100 = df.ta.ema(length=100, append=True)
ema150 = df.ta.ema(length=150, append=True)
keltner = df.ta.kc(append=True)

def in_squeeze(df):
    if df['BBL_5_2.0'] > df['KCLe_20_2'] and df['BBU_5_2.0'] < df['KCUe_20_2'] : 
        return 0 
def out_squeeze(df):
    if not ( df['BBL_5_2.0'] > df['KCLe_20_2'] and df['BBU_5_2.0'] < df['KCUe_20_2']):         
        return 0
    
df['squeeze_on'] = df.apply(in_squeeze, axis=1)
df['squeeze_off'] = df.apply(out_squeeze, axis=1)


mpfdf_columns = list(df.columns)


###################################    PLOT TTM SQUEEZE & EMA21     ###################################

# taplots = [] 
# taplots += 
# Lets start with a simple chart 

# mpfdf = df[-500:-450]
mpfdf = df[-100:]

apsq = [
        # EMA21 ref
        mpf.make_addplot(mpfdf['EMA_21'], type = "scatter", color='blue', markersize=2),  # uses panel 0 by default
        # mpf.make_addplot(mpfdf['EMA_21HA'], color='blue'),  # uses panel 0 by default

        # scatter=True, markersize=3, marker='o',

        # make same as TOS colors 
        mpf.make_addplot(mpfdf[squeezes.columns[-3]], type="bar", color="blue", alpha=0.65, panel=1),
        mpf.make_addplot(mpfdf[squeezes.columns[-4]], type="bar", color="deepskyblue", alpha=0.65, panel=1),
        mpf.make_addplot(mpfdf[squeezes.columns[-2]], type="bar", color="red", alpha=0.65, panel=1),
        mpf.make_addplot(mpfdf[squeezes.columns[-1]], type="bar", color="yellow", alpha=0.65, panel=1),
        # mpf.make_addplot(mpfdf['close'], color="black", panel=1),
        mpf.make_addplot(mpfdf[squeezes.columns[4]], color="green",alpha=0.7, panel=1),
        mpf.make_addplot(mpfdf[squeezes.columns[5]], color="red", alpha=0.7,  panel=1),


        # squeeze metrics 
        mpf.make_addplot(mpfdf[squeezes.columns[2]].apply(lambda x: 0 if x==1 else None ) , scatter=True, markersize=20,marker='o',color="lime",  panel=1),
        
        mpf.make_addplot(mpfdf[squeezes.columns[1]].apply(lambda x: 0 if x==1 else None), scatter=True, markersize=20,marker='o', color="red",  panel=1),
        
        mpf.make_addplot(mpfdf['squeeze_on'], scatter=True,markersize=2,marker='o', color="black",  panel=1),
        # mpf.make_addplot(mpfdf[squeezes.columns[3]], scatter=True,markersize=20,marker='o',color="skyblue",  panel=2),

        # mpf.make_addplot(mpfdf['squeeze_on'].apply(lambda x: -2 if x==0 else None), scatter=True,markersize=10,marker='o', color="black",  panel=1),
        # mpf.make_addplot(mpfdf['squeeze_off'].apply(lambda x: -2 if x==0 else None), scatter=True,markersize=10,marker='o', color="lime",  panel=1),        
        ]
# mpfchart["plot_ratios"] += common_plot_ratio # Required to add a new Panel

final_df = mpfdf # placeholder 

# If HA HeikinAski Charts Enabled ; else remove section
## Generate the HA columns and rename to OHLC
final_df = mpfdf[['HA_open', 'HA_high', 'HA_low', 'HA_close']].copy()
final_df.columns = ['open', 'high', 'low', 'close']
# mpf.plot(df2, type='candle', style='yahoo')


import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from matplotlib.ticker import AutoLocator, MultipleLocator

# fig.tight_layout(h_pad= -1.6)

# fig, axlist = mpf.plot(final_df, type='candle', addplot=apsq, figscale=1, figratio=(15,8),title= symbol+'\nTTM-Squeeze: '+ interval, style='yahoo', volume=False,panel_ratios=(6,2), datetime_format=' %m/%d',xrotation=45, returnfig=True)


fig, axlist = mpf.plot(final_df, type='candle', addplot=apsq, figscale=1, figratio=(15,8),title= symbol+'\nTTM-Squeeze: '+ interval, style='yahoo', volume=False, panel_ratios=(6,2), datetime_format=' %b-%d',xrotation=90, returnfig=True)

ax1 = axlist[1]

ax1.minorticks_on()
ax1.tick_params(axis='x',which='minor',direction='out',color='b',labelsize=3,labelcolor='g')
ax1.xaxis.set_minor_locator(MultipleLocator(1))
# ax1.xaxis.set_major_locator(MultipleLocator(2))

# plt.rcParams['xtick.major.size'] = 8
# plt.rcParams['xtick.minor.size'] = 4
# plt.rcParams['xtick.label.size'] = 4
# ax1.tick_params(axis='x', which='both',labelbottom= False, labeltop=False )
# ax1.tick_params(axis='x', which='minor', pad = 2)
# ax1.grid(which='major',color='k')
# ax1.grid(which='minor',color='gray')

# base = len(final_df)

# ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
# # ax1.xaxis.set_major_locator(mticker.IndexLocator(base=base/10, offset=0))
# ax1.xaxis.set_minor_formatter(mdates.DateFormatter('%d'))
# ax1.xaxis.set_minor_locator(AutoMinorLocator())

# mpf.plot(mpfdf, type='candle', figscale=1, style='blueskies')
plt.show()
print (df[-1:][['open', 'high', 'low', 'close']])
