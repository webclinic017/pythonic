import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

"""This cell defineds the plot_candles function"""

def plot_candles(pricing, title=None, volume_bars=False, color_function=None, technicals=None, h=7, w=10):
    """ Plots a candlestick chart using quantopian pricing data.
    
    Author: Daniel Treiman
    
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
    oc_min = pd.concat([open, close], axis=1).min(axis=1)
    oc_max = pd.concat([open, close], axis=1).max(axis=1)
    
    if volume_bars:
        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, gridspec_kw={'height_ratios': [3,1]})
        fig.set_figheight(h)
        fig.set_figwidth(w)
    else:
        fig, ax1 = plt.subplots(1, 1)
        fig.set_figheight(h)
        fig.set_figwidth(w)
    if title:
        ax1.set_title(title)
    x = np.arange(len(pricing))
    candle_colors = [color_function(i, open, close, low, high) for i in x]
    candles = ax1.bar(x, oc_max-oc_min, bottom=oc_min, color=candle_colors, linewidth=0)
    # lines = ax1.vlines(x + 0.4, low, high, color=candle_colors, linewidth=1)
    lines = ax1.vlines(x, low, high, color=candle_colors, linewidth=1)

    ax1.xaxis.grid(False)
    ax1.xaxis.set_tick_params(which='major', length=3.0, direction='in', top='off')
    # Assume minute frequency if first two bars are in the same day.
    frequency = 'minute' if (pricing.index[1] - pricing.index[0]).days == 0 else 'day'
    time_format = '%m-%d-%Y'
    if frequency == 'minute':
        time_format = '%m%d %H:%M'
    # Set X axis tick labels.
    plt.xticks(x, [date.strftime(time_format) for date in pricing.index], rotation='vertical')
    for indicator in technicals:
        # ax1.plot(x, indicator) # for line plot 
        ax1.plot(x, indicator, 'o', markersize=2) # for scatter plot isolated
        # ax1.plot(x, indicator, marker='o', markersize=5) # for line plot 

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




#######################################################################################
##                                 ALGO CODE 
#######################################################################################

import yfinance as yf
import pandas_ta as ta
#Importing market data
df = yf.download(tickers='AMZN',period = '150d', interval = '1d')
# df = yf.download(tickers='AMZN',period = '50d', interval = '60m')
# df.ta.ha(append=True) # calculate Heikin Ashi ohlc
ema21 = df.ta.ema(length=21, append=True)
ema08 = df.ta.ema(length=8, append=True)


# Simple plain OHLC 
# plot_candles(df[-20:], title='1 day candles', volume_bars=True,) 
# plot_candles(df[-50:], title='1 day candles', volume_bars=True,) # ideal 
# plot_candles(df[-75:], title='1 day candles', volume_bars=True,) 

# Candles with Technical indicators
plot_candles(df[-50:], title='1 day candles', volume_bars=True, technicals=[ema21[-50:], ema08[-50:]])
plot_candles(df[-50:], title='1 day candles', volume_bars=False, technicals=[ema21[-50:], ema08[-50:]])
# plot_candles(df[-80:], title='1 day candles', volume_bars=False, technicals=[ema21[-80:], ema08[-80:]])


#######################################################################################
