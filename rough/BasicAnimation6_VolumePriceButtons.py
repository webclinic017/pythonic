from datetime import date, datetime, time, timedelta

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import mplfinance as mpf
import numpy as np
import pandas as pd
import seaborn as sns
import yfinance as yf
from market_profile import MarketProfile
from matplotlib.widgets import Button
import os 

# Class to simulate getting more data from API:


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
        # print(r1,  self.data_pointer)
        return self.data_frame.iloc[r1:self.data_pointer, :]

    def fetch_prev(self, interval=1):
        r1 = self.data_pointer - interval*2
        self.data_pointer -= interval
        # if self.data_pointer >= self.df_len:
        #     return None
        # print(r1,  self.data_pointer)
        return self.data_frame.iloc[r1:self.data_pointer, :]

    def initial_fetch(self):
        if self.data_pointer > 0:
            return
        r1 = self.data_pointer
        self.data_pointer += int(0.2*self.df_len)
        return self.data_frame.iloc[r1:self.data_pointer, :]


##########      DOWNLOAD YAHOO DATA     #############
symbol = 'AMZN'
sd = datetime(2020, 1, 1)  # sd = datetime(2019, 4, 1)
ed = datetime(2021, 2, 28)
# dfdata = yf.download(tickers=symbol, start=sd, end=ed, interval="60m")
# dfdata.to_pickle(symbol+'.pickle')
# dfdata = pd.read_csv('h:/WorkSpace_Python/AppPy/rough/'+symbol+'.csv', index_col='Datetime', parse_dates=True)
if os.name == 'nt': dfdata = pd.read_pickle('h:/WorkSpace_Python/pythonic/rough/'+symbol+'.pickle')
else: dfdata = pd.read_pickle('/home/towshif/code/python/pythonic/rough/'+symbol+'.pickle')
# dfdata = pd.read_pickle('h:/WorkSpace_Python/AppPy/rough/'+symbol+'.pickle')

dfdata = dfdata.iloc[500:]
print("Read pickle", symbol)

# dfdata['Date'] = dfdata.index
# dfdata['Date'] = dfdata['Date'].dt.tz_localize(None)
# dfdata.set_index('Date', inplace=True)

df = dfdata.copy()

###########  PREPROCESSINNG DF ###############
df['PriceUp'] = df['Close'].gt(df['Open'])
df['VolumeR'] = np.where(df['PriceUp'] == True, df['Volume'], -1*df['Volume'])


# pd.show_versions()

rtapi = RealTimeAPI(df)  # pass a dataframe with OHLCV data in Yahoo format

resample_map = {'Open': 'first',
                'High': 'max',
                'Low': 'min',
                'Close': 'last'}
resample_period = '15T'

df = rtapi.initial_fetch()
# rs = df.resample(resample_period).agg(resample_map).dropna()
rs = df.copy()

# fig, axes = mpf.plot(rs,returnfig=True,figsize=(11,8),type='candle',title='\n\nGrowing Candle')
# ax = axes[0]

fig = plt.figure(figsize=(18, 9))
fig.suptitle(symbol, x=0.01, y=.99, fontsize=20, fontweight='bold', horizontalalignment='left')


# ax = sns.distplot(d.Volume, x=d.Close,hist_kws={'weights':d.Volume}, bins = 100)
# ax = plt.gca() # get currwent axis


# read https://towardsdatascience.com/the-many-ways-to-call-axes-in-matplotlib-2667a7b06e06
ax0 = fig.add_axes([0, 0.1, 0.65, 0.9])
ax1 = fig.add_axes([0.7, 0.1, 0.10, 0.9], sharey=ax0)
ax2 = fig.add_axes([0.8, 0.1, 0.10, 0.9], sharey=ax0)
ax3 = fig.add_axes([0.9, 0.1, 0.10, 0.9], sharey=ax0)

ax0.set_title(symbol + " analysis")
ax0.set_ylabel('')
ax1.get_yaxis().set_visible(False)
ax2.get_yaxis().set_visible(False)
ax2.get_xaxis().set_visible(False)
ax3.get_yaxis().set_visible(False)
ax3.get_xaxis().set_visible(False)


# Create an array with the colors you want to use
# Set your custom color palette
colors = ["#ff3061", "#00b061", "blue", "orange"]
customPalette = sns.set_palette(sns.color_palette(colors))
"Kernel Density Estimator"
kde_factor = 0.05
num_samples = 500
lookback_period = 500
display_period = 200


def animate(forward=True, interval=7):
    global df
    global rs
    global ax0, ax1, ax2, ax3

    if forward:
        nxt = rtapi.fetch_next(interval=interval)  # 7 for whole day 1 h data
        df = df.append(nxt)
        df = df.iloc[1:]
    else:
        nxt = rtapi.fetch_prev(interval=interval)
        # df = df.append(nxt)
        df = df.iloc[1:-interval]

    # if nxt is None:
    #     print('no more data to plot')
    #     ani.event_source.interval *= 3
    #     if ani.event_source.interval > 12000:
    #         exit()
    #     return

    # rs = df.resample(resample_period).agg(resample_map).dropna()
    ax0.clear()
    ax1.clear()
    ax2.clear()
    ax3.clear()

    # mpf.plot(rs[:150],ax=ax0,type='candle', style='yahoo')

    # WORKING ------------------- Plot candles
    mpf.plot(df[-display_period:], ax=ax0,
             type='candle', style='yahoo',  ylabel='')
    ax0.autoscale()
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

    # WORKING ------------------- Plot hist of Up and Down volumes with KDE Peaks
    sns.kdeplot(data=df[-lookback_period:], y='Close', hue="PriceUp", weights=df[-lookback_period:].Volume.astype(
        np.float64), palette=customPalette,  alpha=0.2, bw_method=kde_factor, fill=True, legend=False, ax=ax1)  # normalize Y
    ax1.autoscale()

    # sns.histplot(data=df[-lookback_period:], y='Close', hue="PriceUp", weights=df[-lookback_period:].Volume.astype(np.float64), bins=100, stat="density", palette=customPalette,  alpha=1, kde=True, kde_kws={'bw_method': kde_factor}, ax=ax2) # normalize Y

    # sns.histplot(data=df, y='Close',  weights=df.Volume.astype(np.float64), bins=100, stat="count", color='gray', kde=True, kde_kws={'bw_method': 0.10}, ax=ax2) # normalize Y

    # sns.histplot(data=df[-lookback_period:], y='Close', weights=df[-lookback_period:].Volume.astype(np.float64), bins=100, stat="density", palette=customPalette, fill=False, alpha=1, kde=True, kde_kws={'bw_method': kde_factor}, ax=ax2) # normalize Y

    # WORKING ------------------- Plot hist of volume Sum histograms with KDE peaks
    sns.histplot(data=df[-lookback_period:], y='Close', weights=df.Volume.astype(np.float64), bins=100, stat="density",  color='black',
                 fill=False, alpha=1, kde=True, kde_kws={'bw_method': kde_factor}, line_kws={'color': 'purple'}, ax=ax2)  # normalize Y and need fill-false

    # WORKING -------------------  Plot hist of volume differences
    sns.histplot(data=df[-lookback_period:], y='Close', weights=df.VolumeR.astype(
        np.float64), bins=100, fill=False, hue=df.PriceUp, ax=ax3, legend=False)  # hist
    # sns.displot(df.Volume, y=df.Close, weights=df.VolumeR.astype(np.float64), bins = 50, hue=df.PriceUp, ax=ax3)
    # sns.histplot(data=df[-lookback_period:], y='Close',  weights=df.Volume[-lookback_period:].astype(np.float64), ax=ax2, fill=False, bins=100) # hist
    # sns.kdeplot(data=df[-lookback_period:], y='Close', weights=df.Volume.astype(np.float64), palette=customPalette, fill=False, alpha=0.2, bw_method=kde_factor, ax=ax2) # normalize Y

    ax2.autoscale()

    close = float(df[-1:].Close)
    # print ("Close", close)
    # draw price line
    ax0.axhline(close, ls='--', color='b')
    ax1.axhline(close, ls='--', color='b')
    ax2.axhline(close, ls='--', color='b')
    ax3.axhline(close, ls='--', color='b')

    ax0.text(y=close*1.0005, x=ax0.get_xlim()
             [1]*1.01, s="{:.2f}".format(close), alpha=0.7, color='b')

    # ax = sns.displot(df.Volume, x=df.Close, weights=df.Volume, bins = 50, hue=df.PriceUp) # weight Volume

    # ax0.autoscale()

# ani = animation.FuncAnimation(fig, animate, interval=5)
# pause = False
# # function to play pause
# def onClick(event):
#     global pause

#     if pause:
#         pause = False
#         ani.event_source.start()
#         print ("Button clicked:  RESUME")
#     else :
#         pause = True
#         ani.event_source.stop()
#         print ("Button clicked : PAUSED")

# fig.canvas.mpl_connect('button_press_event', onClick)

# ani = animation.FuncAnimation(fig, animate, interval=250)


# BUTTON PANELS and MANUAL CONTROL
class Index:
    ind = 0

    def __init__(self):
        animate(forward=True, interval=2)
        plt.draw()

    def next(self, event):
        animate(forward=True, interval=2)
        plt.draw()

    def nextfast(self, event):
        animate(forward=True, interval=35)  # 1 week = 49
        plt.draw()

    def prevfast(self, event):
        animate(forward=False, interval=35)  # 1 week = 49
        plt.draw()

    def prev(self, event):
        animate(forward=False, interval=2)
        plt.draw()


callback = Index()

# add buttons to UI
axprev = fig.add_axes([0.8, 0.001, 0.045, 0.05])
axnext = fig.add_axes([0.85, 0.001, 0.045, 0.05])
axprevfwd = fig.add_axes([0.9, 0.001, 0.045, 0.05])
axnextfwd = fig.add_axes([0.95, 0.001, 0.045, 0.05])

bnext = Button(axnext, 'Next >')
bnext.on_clicked(callback.next)
bprev = Button(axprev, '< Prev')
bprev.on_clicked(callback.prev)
bnextfast = Button(axnextfwd, '1 week >')
bnextfast.on_clicked(callback.nextfast)
bprevfast = Button(axprevfwd, '< 1 week')
bprevfast.on_clicked(callback.prevfast)

plt.show()
