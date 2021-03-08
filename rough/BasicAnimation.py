from datetime import date, datetime, time, timedelta

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import mplfinance as mpf
import numpy as np
import pandas as pd
import seaborn as sns
import yfinance as yf
from market_profile import MarketProfile

## Class to simulate getting more data from API:

class RealTimeAPI():
    def __init__(self, df):
        self.data_pointer = 0
        self.data_frame = df
        #self.data_frame = self.data_frame.iloc[0:120,:]
        self.df_len = len(self.data_frame)

    def fetch_next(self):
        r1 = self.data_pointer
        self.data_pointer += 1
        if self.data_pointer >= self.df_len:
            return None
        return self.data_frame.iloc[r1:self.data_pointer,:]

    def initial_fetch(self):
        if self.data_pointer > 0:
            return
        r1 = self.data_pointer
        self.data_pointer += int(0.2*self.df_len)
        return self.data_frame.iloc[r1:self.data_pointer,:]


##########      DOWNLOAD YAHOO DATA     #############
symbol = 'AMD'
sd = datetime(2020, 1, 1)
ed = datetime(2021, 2, 28)
dfdata = yf.download(tickers=symbol, start=sd, end=ed, interval="60m")

df = dfdata.copy()


rtapi = RealTimeAPI(df) # pass a dataframe with OHLCV data in Yahoo format 

resample_map ={'Open' :'first',
               'High' :'max'  ,
               'Low'  :'min'  ,
               'Close':'last' }
resample_period = '15T'

df = rtapi.initial_fetch()
# rs = df.resample(resample_period).agg(resample_map).dropna()
rs = df.copy()

fig, axes = mpf.plot(rs,returnfig=True,figsize=(11,8),type='candle',title='\n\nGrowing Candle')
ax = axes[0]

def animate(ival):
    global df
    global rs
    nxt = rtapi.fetch_next()
    if nxt is None:
        print('no more data to plot')
        ani.event_source.interval *= 3
        if ani.event_source.interval > 12000:
            exit()
        return
    df = df.append(nxt)
    df = df.iloc[1:]
    # rs = df.resample(resample_period).agg(resample_map).dropna()
    ax.clear()
    # mpf.plot(rs[:150],ax=ax,type='candle', style='yahoo')
    mpf.plot(df[:100],ax=ax,type='candle', style='yahoo')
    # ax = sns.distplot(df.Volume, x=df.Close,hist_kws={'weights':df.VolumeR}, bins = 100)


ani = animation.FuncAnimation(fig, animate, interval=50)

mpf.show()

# 
# from IPython.display import HTML
# # HTML(ani.to_html5_video())
# ani._repr_html_() is None
# plt.rc('animation', html='html5')

#########  SAVE AS GIF with imagemagik 
# anim.save('../../files/animation.gif', writer='imagemagick', fps=60)
# Image(url='../../../animation.gif')