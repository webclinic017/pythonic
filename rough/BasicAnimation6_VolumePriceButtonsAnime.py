import os
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
from scipy import signal, stats

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
# df['CloseP'] = 0.5 * (df['Open'] + df['Close']) # typical price 
df['CloseP'] = (df['High'] + df['Low'] + df['Close'])/3  # typical price TP = (High + Low + Close)/3 # seems more accurate peaks 
df.rename(columns = {'Adj Close':'CloseAdj'}, inplace = True) 

Closetype = "CloseAdj"  # this column will be used for Desnity Estimation # adjClose better than CloseP
# Closetype = "CloseP"  # this column will be used for Desnity Estimation # adjClose better than CloseP


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
fig.suptitle(symbol + ':' + Closetype, x=0.01, y=.99, fontsize=20, fontweight='bold', horizontalalignment='left')


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
lookback_period = 1000
display_period = 500


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
    sns.kdeplot(data=df[-lookback_period:], y=Closetype, hue="PriceUp", weights=df[-lookback_period:].Volume.astype(
        np.float64), palette=customPalette,  alpha=0.2, bw_method=kde_factor, fill=False, legend=False, ax=ax1)  # normalize Y
    ax1.autoscale()

    # Working => KED PEAKS and S/R line 

    greenLinex = ax1.lines[0].get_xdata()
    greenLiney = ax1.lines[0].get_ydata()
    peaks,_ = signal.find_peaks(greenLinex)
    gkx = greenLinex[peaks]
    gky = greenLiney[peaks]
    greenLinex = ax1.lines[1].get_xdata()
    greenLiney = ax1.lines[1].get_ydata()
    peaks,_ = signal.find_peaks(greenLinex)
    rkx = greenLinex[peaks]
    rky = greenLiney[peaks]
    # plot on chart : labbs 
    for x,y in zip(gkx,gky): 
        ax1.plot( x, y, 'bo', ms=5, color='g') # add dot to vol chart 
        # ax1.axhline(y, ls='--', color='g') # add hline to main chart 
    # for x,y in zip(rkx,rky): 
    #     ax1.plot( x, y, 'bo', ms=5, color='r') # add dot to vol chart 
    #     # ax1.axhline(y, ls='--', color='g') # add hline to main chart 




    # sns.histplot(data=df[-lookback_period:], y='Close', hue="PriceUp", weights=df[-lookback_period:].Volume.astype(np.float64), bins=100, stat="density", palette=customPalette,  alpha=1, kde=True, kde_kws={'bw_method': kde_factor}, ax=ax2) # normalize Y

    # sns.histplot(data=df, y='Close',  weights=df.Volume.astype(np.float64), bins=100, stat="count", color='gray', kde=True, kde_kws={'bw_method': 0.10}, ax=ax2) # normalize Y

    # sns.histplot(data=df[-lookback_period:], y='Close', weights=df[-lookback_period:].Volume.astype(np.float64), bins=100, stat="density", palette=customPalette, fill=False, alpha=1, kde=True, kde_kws={'bw_method': kde_factor}, ax=ax2) # normalize Y

    # WORKING ------------------- Plot hist of volume Sum histograms with KDE peaks
    sns.histplot(data=df[-lookback_period:], y=Closetype, weights=df.Volume.astype(np.float64), bins=100, stat="density",  color='black', fill=False, alpha=1, kde=True, kde_kws={'bw_method': kde_factor}, line_kws={'color': 'purple'}, ax=ax2)  # normalize Y and need fill-false

    # WORKING -------------------  Plot hist of volume differences
    sns.histplot(data=df[-lookback_period:], y=Closetype, weights=df[-lookback_period:].VolumeR.astype(np.float64), bins=100, fill=False, ax=ax3, legend=False)  # hist with differences 

    # Calculate summ of differences 
    close = float(df[-1:].Close)

    bars = [patch.get_width() for patch in ax3.patches]
    ticks = [patch.get_y() for patch in ax3.patches]
    # for item in zip (ticks, bars) : print (item)
    # [(x,y) if x>120 else 0 for x,y in zip (ticks,bars)] # test filter operations
    sumVolAboveAbove = sum([y*x if x>close else 0 for x,y in zip (ticks,bars)])
    sumVolAbovePos = sum([y*x if x>close and y>0 else 0 for x,y in zip (ticks,bars)])
    sumVolAboveNeg = sum([y*x if x>close and y<0 else 0 for x,y in zip (ticks,bars)])
    sumVolBelowPos = sum([y*x if x<close and y>0 else 0 for x,y in zip (ticks,bars)])
    sumVolbelowNeg = sum([y*x if x<close and y<0 else 0 for x,y in zip (ticks,bars)])
    volRatioAbove = -1* sumVolAboveNeg/sumVolAbovePos if sumVolAbovePos != 0 else 0
    volRatioBelow = -1* sumVolbelowNeg/sumVolBelowPos if sumVolBelowPos != 0 else 0

    # if sumVolumeAbove > 0 : 
    ax3.text(y=close*1.0020, x=ax3.get_xlim()[0]*0.9, s="{:.2f}".format(volRatioAbove), alpha=0.7, color='b')
    ax3.text(y=close*0.995, x=ax3.get_xlim()[0]*0.9, s="{:.2f}".format(volRatioBelow), alpha=0.7, color='b')
    ax3.text(y=close*1.0020, x=ax3.get_xlim()[1]*0.5, s="{:.2f}".format(volRatioBelow-volRatioAbove), alpha=0.7, color='b',)


    # WORKING -------------------  Plot hist of volume +/- on same different axes
    # sns.histplot(data=df[-lookback_period:], y='Close', weights=df[-lookback_period:].VolumeR.astype(np.float64), bins=100, fill=False,  hue=df[-lookback_period:].PriceUp, ax=ax3, legend=False)  # hist with fills 
    # sns.histplot(data=df[-lookback_period:], y='Close', weights=df[-lookback_period:].VolumeR.astype(np.float64), bins=100, fill=False, kde=True, kde_kws={'bw_method': kde_factor}, hue=df[-lookback_period:].PriceUp, ax=ax3, legend=False)  # hist
    # sns.displot(df.Volume, y=df.Close, weights=df.VolumeR.astype(np.float64), bins = 50, hue=df.PriceUp, ax=ax3)
    # sns.histplot(data=df[-lookback_period:], y='Close',  weights=df.Volume[-lookback_period:].astype(np.float64), ax=ax3, fill=False, bins=100) # hist
    # sns.kdeplot(data=df[-lookback_period:], y='Close', weights=df.VolumeR.astype(np.float64), palette=customPalette, fill=False, alpha=0.2, bw_method=kde_factor, ax=ax3) # normalize Y

    ax2.autoscale()

    close = float(df[-1:].Close)
    # print ("Close", close)
    # draw price line
    ax0.axhline(close, ls='--', color='b')
    ax1.axhline(close, ls='--', color='b')
    ax2.axhline(close, ls='--', color='b')
    ax3.axhline(close, ls='--', color='b')

    ax0.text(y=close*1.0005, x=ax0.get_xlim()[1]*1.01, s="{:.2f}".format(close), alpha=0.7, color='b')

    # ax = sns.displot(df.Volume, x=df.Close, weights=df.Volume, bins = 50, hue=df.PriceUp) # weight Volume

    # ax0.autoscale()


#####################  CODE FOR ANIMATION VIEW      #################
# animation object
ani = animation.FuncAnimation(fig, animate, interval=5)
pause = False
# function to play pause
def onClick(event):
    global pause

    if pause:
        pause = False
        ani.event_source.start()
        print ("Button clicked:  RESUME")
    else :
        pause = True
        ani.event_source.stop()
        print ("Button clicked : PAUSED")

fig.canvas.mpl_connect('button_press_event', onClick)



#####################  CODE FOR MANUAL BUTTON CONTROL VIEW      #################


# # BUTTON PANELS and MANUAL CONTROL
# class Index:
#     ind = 0

#     def __init__(self):
#         animate(forward=True, interval=2)
#         plt.draw()

#     def next(self, event):
#         animate(forward=True, interval=2)
#         plt.draw()

#     def nextfast(self, event):
#         animate(forward=True, interval=35)  # 1 week = 49
#         plt.draw()

#     def prevfast(self, event):
#         animate(forward=False, interval=35)  # 1 week = 49
#         plt.draw()

#     def prev(self, event):
#         animate(forward=False, interval=2)
#         plt.draw()


# callback = Index()

# # add buttons to UI
# axprev = fig.add_axes([0.8, 0.001, 0.045, 0.05])
# axnext = fig.add_axes([0.85, 0.001, 0.045, 0.05])
# axprevfwd = fig.add_axes([0.9, 0.001, 0.045, 0.05])
# axnextfwd = fig.add_axes([0.95, 0.001, 0.045, 0.05])

# bnext = Button(axnext, 'Next >')
# bnext.on_clicked(callback.next)
# bprev = Button(axprev, '< Prev')
# bprev.on_clicked(callback.prev)
# bnextfast = Button(axnextfwd, '1 week >')
# bnextfast.on_clicked(callback.nextfast)
# bprevfast = Button(axprevfwd, '< 1 week')
# bprevfast.on_clicked(callback.prevfast)


# always enable at the end 
plt.show()
