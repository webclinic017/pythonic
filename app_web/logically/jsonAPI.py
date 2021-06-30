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

%load_ext autoreload
%autoreload 2

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
updateWatchlistLastUpdated() # DEFAULT watchlist 

data.getWatchlist()
data.getWatchlist(watchlistName='WatchListDBFull.pickle')

# data.createWatchlist(watchlistName='delistedWatchList.pickle', symbols=['MIK'])
download = data.updateDataEOD(interval='1H',persist=False)




######################################################## sanitize watchlist [Notes] 

w = data.getWatchlist()
w
w.loc['MIK']
w.loc['SPY']
# uniquelist
uniquelist = w['end.1H'].unique()
fivedaysago = date.today() - timedelta(days=5)
pp = w[w['end.1H'].isin(uniquelist)]['end.1H']
pp
# add to delist watchlist 
removelist = pp[pp < fivedaysago].index
removelist
# pp[pp['end.1H'] < fivedaysago].index.tolist()
# w[w['end.1H'].isin(removelist)]
w.drop(removelist, inplace = True)
w.loc['MIK']
w.loc['SPY']



data.getupdatedData('CTB', '1h')
data.getupdatedData('MIK', '1h')
data.getupdatedData('GROW', '1h')


# method to remove delisted symbols 
watchlist = getWatchlist()
delist = getWatchlist('delistedWatchList.pickle')

df = watchlist[['end.1H']]
value_counts = df.stack().value_counts() # Entire DataFrame 
threshold = 0.10*value_counts.sum() ## 10% of the total # of instruments 
to_remove = value_counts[value_counts <= threshold].index 
value_counts[value_counts <= 5].index
fivedaysago = datetime.today().date() - timedelta(days=5) # if older than 5 days 
pp = watchlist[watchlist['end.1H'].isin(to_remove)]['end.1H']
removelist = pp[pp < fivedaysago].index
delist = watchlist.loc[removelist] # add to delistwatchlist 
delistwatchList = getWatchlist('delistedWatchList.pickle')
delistwatchList = pd.concat([delistwatchList, delist]) ## add to watchlist 
delistwatchList
delistwatchList = delistwatchList[~delistwatchList.index.duplicated(keep='last')] ## remove duplicates     
delistwatchList
delistwatchList.to_pickle(DATAROOT+'delistedWatchList.pickle') ## persist to disk 
print ( f"Symbol to remove (probably delisted): {removelist}")
# w.loc[removelist]  # add to delistwatchlist 
getWatchlist('delistedWatchList.pickle')


w.drop(removelist, inplace = True)
w.loc['MIK']
w.loc['SPY']
# [ lambda x: datetime.today() -x > timedelta.days(1), to_remove.tolist()]

data.sanitizeWatchlist()
data.sanitizeWatchlist(watchlistName='WatchListLive.pickle')
watchlist
data.saveWatchlist()
data.saveWatchlist(watchlist=watchlist, watchlistName="Hello.pickle")
# data.getWatchlist(watchlistName="Hello.pickle")

data.getWatchlist().loc['MIK'] ## key error 
data.getWatchlist('delistedWatchList.pickle').loc['MIK'] ## key error 

### method to describe frequency of a watchlist 
data.showWatchlist()
data.showWatchlist('delistedWatchList.pickle')
data.showWatchlist('WatchListLive.pickle')

### method to describe frequency of a watchlist 
filter_col = [col for col in watchlist if col.startswith('end')]
df = watchlist[filter_col]
df.stack().value_counts()
df[filter_col].value_counts().index.tolist()
df[filter_col].nunique()



w['end.1H'].min()

data.getData('WSM', '1h')
data.getLiveData(interval='5m', period='1d')

data.downloadData('SPT', "1D")
data.downloadData('AAL', "5m")

data.getData('SPT', '5m')
data.getData('SPY', '5m')

data.getupdatedData('SPT', '1D')
data.getupdatedData('SPT', '5m')
data.getupdatedData('SPT', '1h')
data.getupdatedData('SPY', '1H')
data.getupdatedData('AAL', '1H')

data.downloadData('SPY', '1H')

data.getDataFromPickle('NVDA', '5m')
data.getupdatedData('NVDA', '5m')
download = data.getupdatedData('NVDA', '5m')
download.loc['2021-06-28' :  ].tail(25)
download.loc['2021-06-28 11:30:00'] ## check fro multiple entries 



data.getupdatedData('BK', '1D')
data.getData('JNUG', '1D')

# df = data.updateData('SPT', '5m')
# df.drop(df[(df.index.hour ==16) & (df.index.minute == 0)].index, inplace=True)


#################################           EOD BULK UPDATER 


download = data.updateDataEOD(interval='1D')
download = data.updateDataEOD(interval='1H')
download = data.updateDataEOD(interval='5m')

download, sm = data.loadDatatoMemory('WatchListDBFull.pickle', interval='5m')
download['BK']
data.getDataFromPickle('BK', '1D')
p = data.getupdatedData('BK', '1D')

download['JNUG'].loc['2021-04-15']
download['JNUG'].loc['2021-04-14' : '2021-04-21' ]
download['JNUG'].loc['2021-04-14' :  ]




watchlist = getWatchlist('WatchListDBFull.pickle') # defaults to default watclist 
watchlist
watchlist.loc['BK']
symbols = watchlist.sort_values(by='end.1H', ascending=True).TICK.to_list()
symbols
data.updateDataEODAll(watchlistName='WatchListLive.pickle')

data.updateDataEODAll(watchlistName='WatchListDBFull.pickle')
data.updateDataEODAll()
data.getDataFromPickle('SPT', '1H')
data.getDataFromPickle('AMD', '1H')
data.getDataFromPickle('MIK', '1H')
data.getDataFromPickle('SPY', '5m')
data.getupdatedData('SNA', '5m')
# data.getData('MIK', '1h').dropna()

# import pickle
# df=pickle.load(open(TICKDATA+'SNA.5m.pickle','rb'))

####################### debug 
watchlistName='WatchListDBFull.pickle'
interval='1H'
# get the latest updated watchlist 
watchlist = getWatchlist(watchlistName) # defaults to default watclist 
updateWatchlistLastUpdated(watchlistName) # update entire watchlist first 
showWatchlist(watchlistName)
sanitizeWatchlist(watchlistName)


# sort by time lastupdated and then generate list: to improve performance 
syms = watchlist.sort_values(by='end.'+interval, ascending=True).TICK.to_list()

symArray = list(chunks (syms, 25))  # generate a list of symbol list of length 25 each 
# print ( symArray)

symbols = symArray[0] 

minDate = watchlist.loc[symbols]['end.'+interval].min() 
maxDate = watchlist.loc[symbols]['end.'+interval].max() 
start = minDate.date() - timedelta(days=1) 
end = datetime.today().date() + timedelta(days=1)
# end = maxDate.date() + timedelta(days=5)
print (f"Dates : min {minDate}, max {maxDate}")
print ( f"Watchlist start={start} end={end}, interval: {interval}")


symbols = ['VAR', 'MIK', 'FLIR', 'CTB', 'THI', '^HSI', '^FTSE', '^GDAXI', 'CCS', 'BGFV', 'AMRK', 'AVNW', 'KLIC', 'GSL', 'CALX', 'TBBK', 'LOW', 'LEN', 'GROW', 'CENTA', 'USAK', 'TPX', 'LOB', 'TFII', 'LAD']
# symbols = ['AMD', 'SPY', 'GE']
download = yf.download(tickers=symbols, interval='5m', period='60d', group_by="Ticker")
# df['AMD']
# df.KMB

df['LAD']
# data.getDataFromPickle('KMB', '5m')

df
df['']

ddr = {}
for symbol in symbols : 
    dfdata = getDataFromPickle(symbol, interval=interval)
    d = download[symbol].dropna() ## drop na from extracted df 
    if len (d) > 0 : 
        print ( symbol)
        d = fix_timezone(d) # extract Df from download and fixtimezone
        # Append to the existing dataframe 
        dfdata = pd.concat( [dfdata, d])
        dfdata = dfdata[~dfdata.index.duplicated(keep='first')] # remove duplicated by index
        ddr[symbol] = dfdata  # append to local dict # debub only 



fix_timezone(df)
if len(df)>0: df.drop(df[(df.index.hour ==16) & (df.index.minute == 0)].index, inplace=True)


yf.download(tickers='^HSI', interval='5m', period='60d', group_by="Ticker")

getDataFromPickle('^GSPC', '5m')
getDataFromPickle('^HSI', '5m')
getDataFromPickle('^FTSE', '5m')
getDataFromPickle('^GDAXI', '5m')
