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

    def fetch_next(self, interval=1):
        r1 = self.data_pointer
        self.data_pointer += interval
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
symbol = 'AAPL'
sd = datetime(2020, 1, 1)
ed = datetime(2021, 2, 28)
dfdata = yf.download(tickers=symbol, start=sd, end=ed, interval="60m")

df = dfdata.copy()

###########  PREPROCESSINNG DF ###############
df['PriceUp'] = df['Close'].gt(df['Open'])
df['VolumeR'] =  np.where(df['PriceUp']==True, df['Volume'], -1*df['Volume'])


# pd.show_versions()

rtapi = RealTimeAPI(df) # pass a dataframe with OHLCV data in Yahoo format 

resample_map ={'Open' :'first',
               'High' :'max'  ,
               'Low'  :'min'  ,
               'Close':'last' }
resample_period = '15T'

df = rtapi.initial_fetch()
# rs = df.resample(resample_period).agg(resample_map).dropna()
rs = df.copy()

# fig, axes = mpf.plot(rs,returnfig=True,figsize=(11,8),type='candle',title='\n\nGrowing Candle')
# ax = axes[0]

fig = plt.figure(figsize=(10,6))
# ax = sns.distplot(d.Volume, x=d.Close,hist_kws={'weights':d.Volume}, bins = 100)
# ax = plt.gca() # get currwent axis
ax0 = fig.add_axes ([0, 0, 0.8, 1])
ax = fig.add_axes ( [0.8, 0, 0.2, 1], sharey = ax0) 

# Create an array with the colors you want to use
colors = ["#ff3061", "#00b061","blue", "orange"]# Set your custom color palette
customPalette = sns.set_palette(sns.color_palette(colors))
"Kernel Density Estimator"
kde_factor = 0.05
num_samples = 500

def animate(ival):
    global df
    global rs
    global ax
    nxt = rtapi.fetch_next(interval=2)
    if nxt is None:
        print('no more data to plot')
        ani.event_source.interval *= 3
        if ani.event_source.interval > 12000:
            exit()
        return
    df = df.append(nxt)
    df = df.iloc[1:]
    # rs = df.resample(resample_period).agg(resample_map).dropna()
    ax0.clear()
    ax.clear()
    
    # mpf.plot(rs[:150],ax=ax0,type='candle', style='yahoo')
    mpf.plot(df[-200:],ax=ax0,type='candle', style='yahoo')
    # ax = sns.distplot(df.Volume, x=df.Close,hist_kws={'weights':df.VolumeR}, bins = 100)
    # ax = sns.histplot(data=df, x='Close', hue="PriceUp", weights=df.Volume, bins = 100)
    # ax = sns.histplot(data=df, x='Close', weights=df.Volume, bins = 100)

    # ax = sns.histplot(data=df, x='Close', weights=df.Volume, bins = 50)
    # ax = sns.histplot(data=df, x='Close', weights=df.Volume, bins = 50, stat="density")

    # ax = sns.histplot(data=df, x='Close', hue="PriceUp", weights=df.Volume, bins=50, palette=customPalette,  alpha=1)
    # ax = sns.histplot(data=df, x='Close', hue="PriceUp", weights=df.Volume.astype(np.float64), bins=100, stat="density", palette=customPalette,  alpha=1) # normalize Y 
    # ax = sns.histplot(data=df, x='Close', hue="PriceUp", weights=df.Volume.astype(np.float64), bins=100, stat="density", palette=customPalette,  alpha=1, kde=True) # normalize Y 

    # histogram with KDE     
    # ax = sns.histplot(data=df, y='Close', hue="PriceUp", weights=df.Volume.astype(np.float64), bins=100, stat="density", palette=customPalette,  alpha=1, kde=True, kde_kws={'bw_method': kde_factor}) # normalize Y 
    
    # KDE only 
    # ax = sns.kdeplot(data=df, y='Close', hue="PriceUp", weights=df.Volume.astype(np.float64), palette=customPalette,  alpha=0.2, bw_method=kde_factor, fill=True) # normalize Y 


    # #####  [TESTING PARAMS] KDE only with last 150 
    ax = sns.kdeplot(data=df[-200:], y='Close', hue="PriceUp", weights=df[-200:].Volume.astype(np.float64), palette=customPalette,  alpha=0.2, bw_method=kde_factor, fill=True) # normalize Y 

    
    
    
    
    close = float(df[-1:].Close)
    # print ("Close", close)
    # draw price line 
    ax.axhline(close, ls='--', color='b')
    ax0.axhline(close, ls='--', color='b')
    ax0.text(y=close, x=ax0.get_xlim()[1]*0.70, s="{:.2f}".format(close), alpha=0.7, color='b')

    # ax = sns.displot(df.Volume, x=df.Close, weights=df.Volume, bins = 50, hue=df.PriceUp) # weight Volume 

# ani = animation.FuncAnimation(fig, animate, interval=5)
ani = animation.FuncAnimation(fig, animate, interval=250)

plt.show()

# from IPython.display import HTML
# HTML(ani.to_jshtml())


# 
# from IPython.display import HTML
# # HTML(ani.to_html5_video())
# ani._repr_html_() is None
# plt.rc('animation', html='html5')

#########  SAVE AS GIF with imagemagik 
# anim.save('../../files/animation.gif', writer='imagemagick', fps=60)
# Image(url='../../../animation.gif')