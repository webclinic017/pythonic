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


symbol = 'ZM'
sd = datetime(2021, 1, 1)
ed = datetime(2021, 2, 26)

df = yf.download(tickers=symbol, start=sd, end=ed, interval="60m")
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
mpf.plot(mpfdf, style='yahoo', type='candle', volume=True, panel_ratios=(4,1))


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


mpfdf_columns = list(df.columns)


############   PLOT BOLLINGER BANDS 
mpfdf = df.tail(100)
ap0 = [ mpf.make_addplot(mpfdf['BBU_5_2.0'],color='g'),  # uses panel 0 by default
        mpf.make_addplot(mpfdf['BBL_5_2.0'],color='b'),  # uses panel 0 by default
      ]
mpf.plot(mpfdf, style='yahoo', type='candle',volume=False, addplot=ap0)  

# Adding a new panel specify panel number 
# ap2 = [ mpf.make_addplot(mpfdf['BBU_5_2.0'],color='g',panel=2),  # panel 2 specified
#         mpf.make_addplot(mpfdf['BBL_5_2.0'],color='b',panel=2),  # panel 2 specified
#       ]
# mpf.plot(mpfdf,type='candle',volume=True,addplot=ap2)



############    PLOT MACD (signal, histogram)

mpfdf = df.tail(100)
exp12 = mpfdf['close'].ewm(span=12, adjust=False).mean()
exp26 = mpfdf['close'].ewm(span=26, adjust=False).mean()

macd, histogram, signal = mpfdf['MACD_12_26_9'], mpfdf['MACDh_12_26_9'], mpfdf['MACDs_12_26_9']

apds = [
        # mpf.make_addplot(exp12,color='lime'),
        # mpf.make_addplot(exp26,color='c'),
        mpf.make_addplot(histogram,type='bar',width=0.7,panel=1,
                         color='dimgray',alpha=1,secondary_y=False),
        mpf.make_addplot(macd,panel=1,color='fuchsia',secondary_y=True),
        mpf.make_addplot(signal,panel=1,color='b',secondary_y=True, linestyle='dashed'),
       ]

mpf.plot(mpfdf,type='candle',addplot=apds,figscale=1.1,figratio=(8,5),title='\nMACD',
         style='yahoo',volume=True,volume_panel=2,panel_ratios=(6,3,2))



############    PLOT TTM SQUEEZE 


# taplots = [] 
# taplots += 
mpfdf = df.tail(150)
apsq = [
        mpf.make_addplot(mpfdf[squeezes.columns[-3]], type="bar", color="green", alpha=0.65, panel=1),
        mpf.make_addplot(mpfdf[squeezes.columns[-4]], type="bar", color="lime", alpha=0.65, panel=1),
        mpf.make_addplot(mpfdf[squeezes.columns[-2]], type="bar", color="maroon", alpha=0.65, panel=1),
        mpf.make_addplot(mpfdf[squeezes.columns[-1]], type="bar", color="red", alpha=0.65, panel=1),
        # mpf.make_addplot(mpfdf['close'], color="black", panel=1),
        mpf.make_addplot(mpfdf[squeezes.columns[4]], ylabel="TTM Squeeze", color="green", panel=1),
        mpf.make_addplot(mpfdf[squeezes.columns[5]], color="red",  panel=1),
        ]
# mpfchart["plot_ratios"] += common_plot_ratio # Required to add a new Panel

mpf.plot(mpfdf,type='candle', addplot=apsq, figscale=1.1, figratio=(8,5),title= symbol+'\nTTM-Squeeze', style='yahoo',volume=True,volume_panel=2,panel_ratios=(6,6,2))

############    PLOT EMA 

# Add EMA to Panel 0 - Price 
apsq += [
        mpf.make_addplot(mpfdf['EMA_20'],color='pink'),  # uses panel 0 by default
        mpf.make_addplot(mpfdf['EMA_50'],color='green'),  # uses panel 0 by default
        mpf.make_addplot(mpfdf['EMA_100'],color='orange'),  # uses panel 0 by default
        mpf.make_addplot(mpfdf['EMA_150'],color='red'),  # uses panel 0 by default
        # mpf.make_addplot(mpfdf['EMA_50'],color='b'),  # uses panel 0 by default
    ]

###########     Add Support / Resistance lines 
mpf.plot(mpfdf,hlines=dict(hlines=[400,420],colors=['g','r'],linestyle='dashed'), type='candle', addplot=apsq, figscale=1.1, figratio=(8,5),title= symbol+'\nTTM-Squeeze', style='yahoo',volume=True,volume_panel=2,panel_ratios=(6,6,2))



############    PLOT RSI and RSI_SMA  
baseline = [50.]*len(mpfdf) # RSI 50 
apsq += [        
        mpf.make_addplot(mpfdf['RSI_20'], ylabel="RSI", color="green", panel=2),
        mpf.make_addplot(mpfdf['RSI_20_SMA'], color="orange", panel=2),
        mpf.make_addplot(baseline, color="black", secondary_y=False, panel=2) # add a baseline
        # mpf.make_addplot(mpfdf[squeezes.columns[5]], color="red",  panel=1),
        ]

mpf.plot(mpfdf,hlines=dict(hlines=[400,420],colors=['g','r'],linestyle='dashed'), type='candle', addplot=apsq, figscale=1.1, figratio=(8,5),title= symbol+'\nTTM-Squeeze', style='yahoo',volume=True,volume_panel=3,panel_ratios=(6,4,4,2))



############    PLOT RSX and RSX_SMA  
baseline = [50.]*len(mpfdf)
apsq += [        
        mpf.make_addplot(mpfdf['RSX_20'], ylabel="RSX", color="green", panel=3),
        mpf.make_addplot(mpfdf['RSX_20_SMA'], color="orange", panel=3),
        mpf.make_addplot(baseline, color="black", secondary_y=False, panel=3) # add a baseline
        # mpf.make_addplot(mpfdf[squeezes.columns[5]], color="red",  panel=1),
        ]

mpf.plot(mpfdf,hlines=dict(hlines=[390,440],colors=['g','r'],linestyle='dashed'), type='candle', addplot=apsq, figscale=1.1, figratio=(8,5),title= symbol+'\nTTM-Squeeze', style='yahoo',volume=True,volume_panel=4,panel_ratios=(12,4,4,4,2))


#####       STYLING - line width and others 

setup = dict( style='yahoo', type='candle', volume=True, mav=(7,15,22))
mpf.plot(mpfdf,hlines=dict( hlines=[390,440], colors=['b','b'], linestyle='dashed', linewidths=0.5), addplot=apsq, figscale=1.1, figratio=(8,5),title= symbol+'\nTTM-Squeeze', **setup, volume_panel=4,panel_ratios=(12,4,4,4,2), scale_width_adjustment=dict(ohlc=2.0,lines=0.4))











############        Save as Images 
setup = dict( style='yahoo', type='candle', volume=True, mav=(7,15,22), savefig=dict(fname='tsave100.jpg'))

mpf.plot(mpfdf,hlines=dict( hlines=[390,440], colors=['b','b'], linestyle='dashed', linewidths=0.5), addplot=apsq, figscale=1.1, figratio=(8,5),title= symbol+' : TTM-Squeeze', **setup, volume_panel=4,panel_ratios=(12,4,4,4,2), scale_width_adjustment=dict(ohlc=2.0,lines=0.4))




####################################################################################################################


# mpfchart = {}

# # Create Final Plot
# mpf.plot(mpfdf,
#     title=chart_title,
#     type=mpfchart["type"],
#     style=mpfchart["style"],
#     datetime_format="%-m/%-d/%Y",
#     volume=config["volume"],
#     figsize=mpfchart["figsize"],
#     tight_layout=mpfchart["tight_layout"],
#     scale_padding=mpfchart["scale_padding"],
#     panel_ratios=mpfchart["plot_ratios"], # This key needs to be update above if adding more panels
#     xrotation=mpfchart["xrotation"],
#     update_width_config=mpfchart["width_config"],
#     show_nontrading=mpfchart["non_trading"],
#     vlines=vlines_,
#     addplot=taplots
)