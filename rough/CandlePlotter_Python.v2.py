import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

"""This cell defineds the plot_candles function"""

def plot_candles(pricing, title=None, volume_bars=False, color_function=None, technicals=None, h=7, w=10, secondary=True, showlines=False, ha=False, add_candle_percent=False):
    """ Plots a candlestick chart using quantopian pricing data.
    
    Author: Daniel Treiman
    Co Author: Towshif Ali 
    
    Args:
      pricing: A pandas dataframe with columns ['open', 'close', 'high', 'low', 'volume']
      title: An optional title for the chart
      volume_bars: If True, plots volume bars
      color_function: A function which, given a row index and price series, returns a candle color.
      technicals: A list of additional data series to add to the chart.  Must be the same length as pricing.
    """
    def default_color(index, open, close, low, high):
        return 'r' if open[index] > close[index] else 'g'
    color_function = color_function or default_color
    technicals = technicals or []
    open = pricing['open']
    close = pricing['close']
    low = pricing['low']
    high = pricing['high']
        
    if ha and 'HA_open' in df.columns : # if heikin ashi candles is True (pandas_ta format)
        open = pricing['HA_open']
        close = pricing['HA_close']
        low = pricing['HA_low']
        high = pricing['HA_high']

    oc_min = pd.concat([open, close], axis=1).min(axis=1)
    oc_max = pd.concat([open, close], axis=1).max(axis=1)
    
    if volume_bars:
        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, gridspec_kw={'height_ratios': [3,1]})
        fig.set_figheight(h)
        fig.set_figwidth(w)
    else:
        fig, ax1 = plt.subplots(1, 1)
        # plt.tight_layout() # disable is margin requirements are relaxed
        fig.set_figheight(h)
        fig.set_figwidth(w)
    if title:
        ax1.set_title(title)

    x = np.arange(len(pricing))
    # candle color
    candle_colors = [color_function(i, open, close, low, high) for i in x]
    # draw candle bar : Note 0.01 added to have a visible bar incase open==close ie. oc_max-oc_mi=0 
    candles = ax1.bar(x, 0.01+ oc_max-oc_min, bottom=oc_min, color=candle_colors, linewidth=0)
    
    # lines = ax1.vlines(x + 0.4, low, high, color=candle_colors, linewidth=1)
    lines = ax1.vlines(x, low, high, color=candle_colors, linewidth=1)

    # ax1.xaxis
    ax1.xaxis.grid(False) # xgridline OFF
    # ax1.xaxis.set_tick_params(which='major', length=3.0, direction='in', top='off')
    ax1.xaxis.set_tick_params(which='major', length=3.0, direction='out')
    ax1.set_axisbelow(True) # place gridlines in background 

    # Assume minute frequency if first two bars are in the same day.
    frequency = 'minute' if (pricing.index[1] - pricing.index[0]).days == 0 else 'day'
    time_format = '%m-%d-%Y'
    if frequency == 'minute':
        time_format = '%m%d %H:%M'
    
    # Set X axis tick labels.
    plt.xticks(x, [date.strftime(time_format) for date in pricing.index], rotation='vertical', fontsize=8)
    if len(technicals) != 0 : 
        for indicator in technicals:
            if showlines: 
                ax1.plot(x, indicator,label=indicator.name) # for line plot 
            else : 
                ax1.plot(x, indicator, 'o', markersize=2, label=indicator.name) # for scatter plot isolated
            # ax1.plot(x, indicator, marker='o', markersize=5) # for line plot 
        plt.legend(loc="lower right")

    # Set primary axis y-grid 
    ax1.yaxis.grid(True, color='#EEEEEE',) # very light gray 

    # Set secondary Y axis as percentage 
    ymax, ymin = high.max(), low.min()
    ## convert to percentage in lambda fucntions 
    y2 = ax1.secondary_yaxis('right',functions=(lambda y: (y/ymin - 1) *100, lambda y: y*ymin/100 + ymin ))
    import matplotlib.ticker as mtick
    y2.yaxis.set_major_formatter(mtick.PercentFormatter())

    # Volume Bars 
    if volume_bars:
        volume = pricing['volume']
        volume_scale = None
        scaled_volume = volume
        if volume.max() > 1000000:
            volume_scale = 'M'
            scaled_volume = volume / 1000000
        elif volume.max() > 1000:
            volume_scale = 'K'
            scaled_volume = volume / 1000
        ax2.bar(x, scaled_volume, color=candle_colors)
        volume_title = 'Volume'
        if volume_scale:
            volume_title = 'Volume (%s)' % volume_scale
        ax2.set_title(volume_title)
        ax2.xaxis.grid(False)

    # add candlestick percentage change labels per candle 
    if add_candle_percent : _add_candlestick_labels(ax1, pricing)

    return fig

### Example of plotting with scatter and lines 
### https://jakevdp.github.io/PythonDataScienceHandbook/04.02-simple-scatter-plots.html
### https://www.tutorialspoint.com/matplotlib/matplotlib_scatter_plot.htm
### marker types: [ 'o', '.', ',', 'x', '+', 'v', '^', '<', '>', 's', 'd' ]
# plt.plot(x, y, '-p', color='gray',
#          markersize=15, linewidth=4,
#          markerfacecolor='white',
#          markeredgecolor='gray',
#          markeredgewidth=2)
# plt.ylim(-1.2, 1.2);    
# 
def _add_candlestick_labels(ax, ohlc):
    transform = ax.transData.inverted()
    # show the text 10 pixels above/below the bar
    text_pad = transform.transform((0, 10))[1] - transform.transform((0, 0))[1]
    percentages = 100. * (ohlc.close - ohlc.open) / ohlc.open
    kwargs = dict(horizontalalignment='center', color='#000000', fontsize=7)
    for i, (idx, val) in enumerate(percentages.items()):
        if val != np.nan:
            row = ohlc.loc[idx]
            open = row.open
            close = row.close
            if open < close:
                ax.text(i, row.high + text_pad, np.round(val, 1), verticalalignment='bottom', **kwargs)
            elif open > close:
                ax.text(i, row.low - text_pad, np.round(val, 1), verticalalignment='top', **kwargs)


#######################################################################################
##                                 ALGO CODE Example                                 ##  
#######################################################################################

import yfinance as yf
import pandas_ta as ta

# show only 2 decimal placed on display of dataframe
pd.options.display.float_format = '{:,.2f}'.format  

#Importing market data
df = yf.download(tickers='AAL',period = '150d', interval = '1d')
# df = yf.download(tickers='AAPL',period = '150d', interval = '1d')
# df = yf.download(tickers='SPY',period = '150d', interval = '1d')
# df = yf.download(tickers='QQQ',period = '150d', interval = '1d')
# df = yf.download(tickers='AAL',period = '50d', interval = '90m')
# df = yf.download(tickers='AMD',period = '50d', interval = '60m')
# df = yf.download(tickers='AMZN',period = '50d', interval = '60m')
# df = yf.download(tickers='AMZN',period = '50d', interval = '60m')
# df = yf.download(tickers='GE',period = '50d', interval = '60m')
# df = yf.download(tickers='WGO',period = '50d', interval = '60m')
# df = yf.download(tickers='AMZN',period = '10d', interval = '5m')
# df.ta.ha(append=True) # calculate Heikin Ashi ohlc
ema21 = df.ta.ema(length=21, append=True)
ema08 = df.ta.ema(length=8, append=True)
keltner2 = df.ta.kc(scalar=2, append=True) # 
keltner3 = df.ta.kc(scalar=3, append=True) # 
hashi = df.ta.ha(append=True) # heikin ashi bars 

title = '' + str(df[-1:].iloc[0].close.round(2))

# Simple plain OHLC 
# plot_candles(df[-20:], title=title, volume_bars=True,) 
# plot_candles(df[-50:], title=title, volume_bars=True,) # ideal 
# plot_candles(df[-50:], title=title, volume_bars=False,) 
# plot_candles(df[-50:], title=title, volume_bars=False, ha=True, add_candle_percent=True) 
# plot_candles(df[-75:], title=title, volume_bars=False,) 
# plot_candles(df[10:150], title=title, volume_bars=False,) 

# Candles with Technical indicators
# plot_candles(df[-50:], title=title, volume_bars=True, technicals=[ema21[-50:], ema08[-50:]])
# plot_candles(df[-50:], title=title, volume_bars=False, technicals=[ema21[-50:], ema08[-50:]], showlines=False, add_candle_percent=True)
# plot_candles(df[-50:], title=title, volume_bars=False, technicals=[ema21[-50:], ema08[-50:]], showlines=True, ha=True, add_candle_percent=True)

# plot_candles(df[-50:], title=title, volume_bars=True, technicals=[ema21[-50:], ema08[-50:]], showlines=True, ha=False, add_candle_percent=True)


# plot_candles(df[-50:], title=title, volume_bars=False, showlines=True, ha=True,add_candle_percent=True, 
#     technicals=[
#         ema21[-50:], 
#         ema08[-50:], 
#         df['KCUe_20_2.0'][-50:], 
#         df['KCUe_20_3.0'][-50:]
#         ]
#     )
        
# plot_candles(df[-80:], title=title, volume_bars=False, technicals=[ema21[-80:], ema08[-80:]])


#######################################################################################


################################## TRANSPORT IMAGE OVER SOCKET ########################################
import base64
import io
from flask_socketio import emit, SocketIO


image = plot_candles(df[-50:], title=title, volume_bars=False, technicals=[ema21[-50:], ema08[-50:]], showlines=True, ha=False, add_candle_percent=True)

buf = io.BytesIO()
image.savefig(buf, format="png", dpi=100, pad_inches= 0, transparent=True)
base64_img = base64.b64encode(buf.getbuffer()).decode("ascii")

socketio = SocketIO(message_queue='redis://localhost:6379/')
socketio.emit('chartupdate', {'chart':"data:image/png;base64,"+ base64_img, 'tick': "New Image"})

# #######################################################################################

