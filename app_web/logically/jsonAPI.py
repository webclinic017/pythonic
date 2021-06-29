## jsonAPI.py
## This is a ohlc, indicator, trigger API to be consumed by JS, HTML in conjunction to trading view - lightweight charts library 

####    List of Tasks 
##################################################
#   basic API ->                ohlc, volume API 
#   squeeze API ->              1 histogram (color codes), 1 marker series (color codes)
#   marker signals ->           5+ marker series (color codes) 
#   signal ohlc markers ->      over below ohlc (primary, secondary, final)
#   multitimeframe 4H,1H, 1D    plots markers 
#   visual indicator -> 
#                   Type #1:    2 lines, 1 hist, 1 marker       ::  WaveTrend, MACD, VPCI
#                   Type #2:    3 lines, 1 marker               ::  Volatility, 
#                   Type #3:    2 lines, 2 hist, 3 marker       ::  Koncorde4.0, 
#                   Type #4:    4 lines, 1 marker               ::  SI+Bands (+Zones)
#   Filter timeframe API ->   

import os
import queue
import time
from datetime import date, datetime, timedelta

import finta as ft
import numpy as np
import pandas as pd
import pandas_ta as ta
import yfinance as yf

import genericProcessConsumerPool as processThread  # # communicate using q
import datasource as data
from datasource import *  ### import all variables and methods # dont use in production

# %load_ext autoreload
# %autoreload 2

ddr, symbols = data.loadDatatoMemory(interval='1D') 
ddr['SAIA']

d = ddr['SAIA']
ddr['AMD'].iloc[-1]
d.iloc[-1]
start = d.index[0] # first datetime index 
end = d.index[-1] # last datetime index 

# data.getData('AMD', '1D').tail()
watchlistName = "WatchListDB.pickle"  # initialize
watchlist = pd.read_pickle(DATAROOT + watchlistName ) # read file  
# watchlist['id'] = watchlist['TICK']
# watchlist.set_index('id', inplace=True)  
# watchlist.loc['AMD']['start' + '1H'] = start
# watchlist.loc['AAL', ['start.' + '1H', 'end.' +'1H']] = [start, end]
# watchlist.at['AAL', 'start' + '1H'] = start 
watchlist

updateWatchlistLastUpdated(watchlistName='WatchListDBFull.pickle')
updateWatchlistLastUpdated(watchlistName='WatchListLive.pickle')
updateWatchlistLastUpdated()

data.getWatchlist()
w = data.getWatchlist()
w['end.1H'].min()

data.getData('SPT', '1h')
data.getLiveData(interval='5m', period='1d')

data.downloadData('SPT', "1D")
data.downloadData('AAL', "5m")

data.getData('SPT', '5m')
data.getData('SPY', '5m')

data.updateData('SPT', '1D')
data.updateData('SPT', '5m')
data.updateData('SPT', '1h')
data.updateData('SPY', '1H')
data.updateData('AAL', '1H')
data.updateData('AAL', '1D')
data.getData('JNUG', '1D')

# df = data.updateData('SPT', '5m')
# df.drop(df[(df.index.hour ==16) & (df.index.minute == 0)].index, inplace=True)

download = data.updateDataEOD(interval='1D')
download = data.updateDataEOD(interval='1H')
download = data.updateDataEOD(interval='5m')

download['JNUG'].loc['2021-04-15']
download['JNUG'].loc['2021-04-14' : '2021-04-21' ]
download['JNUG'].loc['2021-04-14' :  ]

data.updateDataEODAll()

data.getDataFromPickle('SPY', '1D')