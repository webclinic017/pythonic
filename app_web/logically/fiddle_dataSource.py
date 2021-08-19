## dataSource_fiddle.py
## This script is to fiddle with datasource module 
#       datasource 
#       updater  


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


############################     data consistency 


interval='5m' ; symbol='MSFT' ; 
# dfdata = yf.download(tickers=symbol, interval=interval, period='730d')
dfdata = getDataFromPickle(symbol=symbol, interval=interval) # read pickle 
data.dataConsistencyCheck(dfdata, interval)



interval='1H'
symbol='WGO'
dfdata = getDataFromPickle(symbol=symbol, interval=interval) # read pickle 
cinterval = {
"1D"    : 1,
"1d"    : 1,
"1h"    : 7,
"1H"    : 7,
"5m"    : 78,
"4H"    : 2,
}
expCount = cinterval.get(interval, None) # expected count 

# check freq by day 
anal = dfdata.groupby(pd.Grouper(freq='D')).count()    
uniqlist=anal['Open'].unique().tolist()
uniqlist.remove(0) # remove entries/days with no data 
uniqlist.remove(expCount) # remove entries/days with expected data count 7 for 1h 
flist = anal.loc[anal['Open'].isin(uniqlist)] # print the unique days 
if len(flist) >0 : print (f"Found outlier data in {symbol}", flist)
else: print (f"{symbol} data consistent.")


## KLAC data inconsistent 
locateDate = '2021-08-02'
yf.download(tickers='KLAC', interval='1h', period="100d").loc[locateDate].tail(70)
data.getDataFromPickle(symbol='KLAC', interval='1h').loc[locateDate].tail(70)






#############           Generating indicator calculations       ##################
from computeIndicator import * 
ddr, symbols = data.loadDatatoMemory(interval='5m') 
ddr, symbols = data.loadDatatoMemory(interval='4H', filter=10) 

len(ddr)

inDict = compute_all_seq(ddr,symbols) # dict of indicators updated 

inDict['AMD'] # check 



ddr['SAIA']
ddr['AMD']

DATAROOT

d = ddr['SAIA']
ddr['AMD'].iloc[-1]
d.iloc[-1]
start = d.index[0] # first datetime index 
end = d.index[-1] # last datetime index 

#####################################   WATCHLIST OPERATIONS    ####################################

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
data.getWatchlist(watchlistName='delistedWatchList.pickle')

# data.createWatchlist(watchlistName='delistedWatchList.pickle', symbols=['MIK'])
download = data.updateDataEOD(interval='1H',persist=False)

d = data.getWatchlist()

## search watchlist 
'SPT' in d.index.tolist() # True or False 

watchlist = data.getWatchlist()
data.searchWatchlist(symbols=['SPT', 'AAL'])

s = ['AMD', 'AAL']
s.append('AAPL')
s
watchlist.loc[s]


##########      MERGE WATCHLIST 
data.getWatchlist(watchlistName='WatchListDBFull.pickle')
data.getWatchlist()
data.mergeWatchList(source=["WatchListDB.pickle", "WatchListLive.pickle"], destination="WatchListDBFull.pickle")
data.getWatchlist(watchlistName='WatchListDBFull.pickle')





######################################################## sanitize watchlist [Notes] 

w = data.getWatchlist(watchlistName="WatchListDBFull.pickle")
w
w.loc['MIK']
w.loc['SPY']
# uniquelist
uniquelist = w['end.1H'].unique()
uniquelist
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



data.getUpdatedData('CTB', '1h')
data.getUpdatedData('MIK', '1h')
data.getUpdatedData('GROW', '1h')



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


### getData tests and Download functions 
w['end.1H'].min()

data.getData('WSM', '1h')
data.getLiveData(interval='5m', period='1d')

data.downloadlastEODData('SPT', "1D")
data.downloadlastEODData('AAL', "5m")

data.getData('SPT', '5m')
data.getData('SPY', '5m')

data.getUpdatedData('SPT', '1D')
data.getUpdatedData('SPT', '5m')
data.getUpdatedData('SPT', '1h')
data.getUpdatedData('SPY', '1H')
data.getUpdatedData('AAL', '1H')



#### new data download 
data.downloadlastEODData('SPY', '1H')

dfdata = data.getDataFromPickle('NVDA', '5m')
dfdata = fix_timezone(dfdata)
dfdata[(dfdata.index.hour ==16) & (dfdata.index.minute == 0)].index

data.getUpdatedData('NVDA', '5m')
download = data.getUpdatedData('NVDA', '5m')
download.loc['2021-06-28' :  ].tail(25)
download.loc['2021-06-28 11:30:00'] ## check fro multiple entries 


data.getData('SPT', '4H') # not in database output 

data.downloadlastEODData('SPY', '1H') # not in database output 


data.downloadlastEODData('SPT', '1H') # not in database output 
data.downloadlastEODData('SPT', '5m') # not in database output 
getDataFromPickle(symbol='SPT', interval='1H') # read pickle 
getDataFromPickle(symbol='SPT', interval='5m') # read pickle 
getDataFromPickle(symbol='SPT', interval='1D') # read pickle 


data.inWatchlist('SPT')
data.downloadlastEODData('SPT', '1H') # not in database output 
data.inWatchlist('SPT', watchlistName="WatchListDBFull.pickle")


addToWatchlist(['SPT'])
data.inWatchlist('SPT', "WatchListDBFull.pickle")
data.getWatchlist("WatchListDBFull.pickle").tail()

symbols = ['SPT']
watchlistName="WatchListDBFull.pickle"
watchlist = pd.read_pickle(DATAROOT + watchlistName ) # read file
watchlist = watchlist.append(pd.DataFrame(symbols, columns=['TICK']), ignore_index=True)
watchlist
watchlist['id'] = watchlist['TICK']
watchlist

watchlist.set_index('id', inplace=True)  # prevent duplicates
watchlist = watchlist[~watchlist.index.duplicated(keep='first')]
print (watchlist.tail())


data.searchWatchlist(['SPT'], "WatchListDBFull.pickle")

data.downloadlastEODData('SPT', '5m') 

d = data.getDataFromPickle('SPT', '1h') 
data.dataConsistencyCheck(dfdata=d, interval='1h')
d.loc['2021-06-28'].tail()

### update lastEOD data for a symbol see method 
dfdata = getDataFromPickle(symbol='AMD', interval='5m') # read pickle 
dfdata = getDataFromPickle(symbol='AMD', interval='1H') # read pickle 
dfdata.tail(20)
# dfdata = dfdata[:-42]
dfdata.tail(20)


end = dfdata.index[-1]  # get last timestamp
end.date() < datetime.today().date() - timedelta(days=1)
end.date() < (datetime.today().date() - timedelta(days=1))

start = end.date()
end =  datetime.today().date() # + timedelta(days=1)
print (start, end)
d = yf.download(tickers='AMD', interval='5m', period="60d")
d.loc['2021-06-25'].tail(70)
yf.download(tickers='AMD', interval='5m', start=start).loc['2021-06-29'].tail(70)




################################         test resampling 

data.gen4HdataFromPickle('SPY').tail(20)
data.gen4HdataFromPickle('SPT')
data.getData('SPY')

data.gen4HdataFromPickle('AMD').tail(20) # default from source is 1H 
data.generateResampledData('AMD', '3.5H', frominterval='1H').tail(20)  ## 4H resample schemes : 3 samples/dayr
data.generateResampledData('AMD', '3.75H', frominterval='1H').tail(20)  ## 4H resample schemes 
data.generateResampledData('AMD', '2.5H', frominterval='1H').tail(20)  ## 4H resample schemes 
data.getDataFromPickle('AMD', '1H').tail(20)


data.generateResampledData('SPY', '4H', frominterval='5m').tail(20)
data.generateResampledData('SPY', '1D', frominterval='1H').tail(20)
data.getDataFromPickle('SPY', '1D').tail(20)
data.getDataFromPickle('SPY', '1H').tail(20)
data.getDataFromPickle('SPY', '5m').tail(20)

import yfinance as yf
# pip install yfinance -U--no-cache-dir  # upgrade required to v *.62 
## debug behavior from yf 
yf.download(tickers='SPY', interval='1h', period='5d', prepost=True).tail(20)  ## check additional
yf.download(tickers='SPY', interval='1D', period='5d', prepost=True).tail(20)  ## check additional
yf.download(tickers='SPY', interval='1WK', period='5d', prepost=True).tail(20)  ## check additional


data.getUpdatedData('BK', '1H')
data.getUpdatedData('SPY', '5m').tail(20)
data.getData('JNUG', '1D')
data.getData('JNUG', '1H')
data.getTodayOnly(symbolsList=['AAL'], interval='5m')

data.getTodayAll(['AAL'], {})
# df = data.updateData('SPT', '5m')
# df.drop(df[(df.index.hour ==16) & (df.index.minute == 0)].index, inplace=True)


#################################           EOD BULK UPDATER 


##############################
data.updateDataEODAll() # default watchlist 
data.updateDataEODAll(watchlistName='WatchListLive.pickle', chunksize=25) #default chunksize=25
data.updateDataEODAll(watchlistName='WatchListDBFull.pickle', chunksize=100)
#################################
data.getWatchlist(watchlistName='delistedWatchList.pickle')
#################################

d = data.getWatchlist(watchlistName='WatchListDBFull.pickle')
ll = ['SPY', 'CCS', 'BGFV', 'AMRK', 'HZNP', 'AVNW', 'KLIC', 'GSL', 'CALX', 'WGO', 'TBBK', 'SYNA', 'LOW', 'LEN', 'CENTA', 'USAK', 'TPX', 'LOB', 'TFII', 'LAD', 'KIRK', 'ABG', 'GROW', 'AMAT', 'HIBB']

d.loc[ll]





data.updateDataEODAll() # default watchlist 
data.getDataFromPickle('AMD', '4H')
data.getDataFromPickle('AMD', '1D')
data.getDataFromPickle('AMD', '1H')
data.getDataFromPickle('AMD', '5m')

dd = data.getDataFromPickle('AMD', '1H')
data.generate4Hdata(dd)



download = data.updateDataEOD(interval='1D')
download = data.updateDataEOD(interval='1H')
download = data.updateDataEOD(interval='5m')




download, sm = data.loadDatatoMemory('WatchListDBFull.pickle', interval='5m')
download['BK']
data.getDataFromPickle('BK', '1D')
p = data.getUpdatedData('BK', '1D')

download['JNUG'].loc['2021-04-15']
download['JNUG'].loc['2021-04-14' : '2021-04-21' ]
download['JNUG'].loc['2021-04-14' :  ]

dfdata = getDataFromPickle('SPT')
dfdata

watchlist = getWatchlist('WatchListDBFull.pickle') # defaults to default watclist 
watchlist
watchlist.loc['BK']
symbols = watchlist.sort_values(by='end.1H', ascending=True).TICK.to_list()
symbols
data.updateDataEODAll(watchlistName='WatchListLive.pickle')

data.updateDataEODAll(watchlistName='WatchListDBFull.pickle')
data.updateDataEODAll()
data.updateWatchlistLastUpdated()

data.getDataFromPickle('SPY', '5m').loc['2021-06-29'].tail()


##############################          DIAGNOSTICS 

data.getDataFromPickle('SPT', '1D')
data.getDataFromPickle('AMD', '1H')
data.getDataFromPickle('MIK', '1H')
data.getDataFromPickle('SPY', '5m')
data.getUpdatedData('SNA', '5m')
# data.getData('MIK', '1h')
data.getUpdatedData('MIK', '1h')
data.getUpdatedData('THI', '1D')

# import pickle
# df=pickle.load(open(TICKDATA+'SNA.5m.pickle','rb'))

##############################                  debug 
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

## foreign -> fix_timezone will not work for these instruments. 
getDataFromPickle('^HSI', '5m')
getDataFromPickle('^FTSE', '5m')
getDataFromPickle('^GDAXI', '5m')



#######################################   LIVE UPDATES (need to run with scheduler)

ddr, symbols = data.loadDatatoMemory(interval='1H')
# symbols[:10]
finaldict = data.getTodayAll(symbolsList=symbols[:10], dfdict=ddr, interval='1H', prepost=True)

ddr['AAPL']
finaldict['AAPL'].tail(20)

# yf.download(tickers='AAPL', interval='90m', period='700d')
ddr['AAPL']

for symbol, df  in ddr.items(): 
    print (symbol , "\t\t" , len(df))

start = datetime.today().date()
start = datetime

symbols = ['AMD', 'AAPL', 'BK']
rtd = yf.download(tickers=symbols, interval='5m', start=start, group_by="Ticker")
rtd ['AMD']



#### more tests on live using prepost function offline 

# test today + old = todayAll()
import random 
interval='1H'
ddr, symbols = data.loadDatatoMemory(interval=interval)
random.shuffle(symbols)
finaldict = data.getTodayAll(symbolsList=symbols[:10], dfdict=ddr, interval=interval, prepost=True)
symbols[:10]
rsymbol = symbols[6:7][0] # select a random symbol from shuffled list 
print(rsymbol)

ddr[rsymbol]
finaldict[rsymbol]


import random 
interval='5m'
ddr, symbols = data.loadDatatoMemory(interval=interval)
random.shuffle(symbols)
finaldict = data.getTodayAll(symbolsList=symbols[:10], dfdict=ddr, interval=interval, prepost=True)
symbols[:10]
rsymbol = symbols[6:7][0] # select a random symbol from shuffled list 
print(rsymbol)

ddr[rsymbol]
finaldict[rsymbol]


# test todayOnly()
import random 
interval='5m'
ddr, symbols = data.loadDatatoMemory(interval=interval)

random.shuffle(symbols)
finaldict = data.getTodayOnly (symbolsList=symbols,interval=interval, prepost=False, chunksize=100)

rsymbol = symbols[6:7][0] # select a random symbol from shuffled list 
print(rsymbol)

finaldict[rsymbol]
finaldict.keys()  # all symbol names 
finaldict['AAPL']
