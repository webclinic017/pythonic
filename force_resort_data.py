"""
Script to Validate entire database.
All pickles will be rewritten. Backup data before use.
Use this with caution. This action cannot be reversed.
"""

import pandas as pd
from datetime import date
import app_web.logically.datasource as data
import random
import os.path, time

## This operation cannot be reversed, use with caution!
data.force_sort_index_all(persist=True)


# Debug 
date.today().year   
symbol='^GSPC'
interval='1H'
dfdata = data.getDataFromPickle(symbol=symbol, interval=interval) # read 
outlierData = data.dataConsistencyCheck(dfdata, interval, verbose=True).loc['2021':]

# Debug 
# find last business day
import pandas_market_calendars as mcal
from datetime import datetime, time, timedelta
import  pytz

eastern = pytz.timezone('US/Eastern')
nyseCal = mcal.get_calendar('NYSE')
cal = nyseCal.schedule(start_date= datetime.today() - timedelta(days=10), end_date=datetime.today())

# Check if market is open 
nytime = datetime.today().now(eastern)
lastOpen = cal.iloc[-1].market_open.tz_convert(eastern)
lastClose =  cal.iloc[-1].market_close.tz_convert(eastern)
print (f"Last Open: {lastOpen}, Last Close {lastClose} | time now {nytime}")

if nytime > lastClose : # Market is closed  
    lastBusinessDate = cal.iloc[-1].market_close.tz_localize(None).to_pydatetime().date()
    print (f"Market Closed. Last business date: {lastBusinessDate}") 

else: # Market is open 
    lastBusinessDate = cal.iloc[-2].market_close.tz_localize(None).to_pydatetime().date()
    print (f"Market Open. Last business (Previous Close)  :{lastBusinessDate}") 

print (lastBusinessDate)

# cal.iloc[-2:]
# cal.iloc[-2]
# cal.iloc[-1]
# cal
# cal.iloc[-1].market_open.tz_localize(None).to_pydatetime()
# datetime.today().now(eastern) > cal.iloc[-1].market_open.tz_localize(None).to_pydatetime()





# test 

symbols = ['SPT', 'LB', 'SPY', 'MPC', 'MAR', 'MMC', 'MLM', 'MAS', 'MA', 'MAT', 'MKC', 'MCD', 'MCK', 'MDT', 'MRK', 'MRO', 'M', 'MAC', 'MTB', 'LYB', 'L', 'LMT', 'LKQ', 'LNC', 'LLY', 'LEG', 'LH', 'KR', 'KHC', 'KSS', 'KMI', 'MET', 'MTD', 'MGM', 'MCHP', 'NUE', 'NRG', 'NCLH', 'NOC', 'NTRS', 'NSC', 'JWN', 'NI', 'NKE', 'NLSN', 'NEE', 'NWS', 'NWSA', 'NEM', 'NWL', 'NTAP', 'NAVI', 'NOV', 'NDAQ', 'MSI', 'MOS', 'MS', 'MCO', 'MNST', 'MON', 'MDLZ', 'TAP', 'MHK', 'MAA', 'KIM', 'KMB', 'KEY', 'K', 'HPE', 'HES', 'HSY', 'HSIC', 'HP', 'HCA', 'HAS', 'HIG', 'HOG', 'HBI', 'HAL', 'GWW', 'GT', 'GS', 'GPN', 'GILD', 'GPC', 'GM', 'GIS', 'GE', 'GD', 'IT', 'GRMN', 'GPS', 'FCX', 'BEN', 'FBHS', 'FTV', 'F', 'HLT', 'ORLY', 'HOLX']

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import datasource as data

# yf.download(tickers=symbols, interval='1D', period='3d', group_by="Ticker") # check connection

##################   Understand yfinance library and API behavior  ##################

# # Need to know: This downloads till 2017-04-28 NOT 2017-04-30 | yahoo downloads till end-1 day
# yf.download("SPY", start="2017-01-01", end="2017-04-30")

## Basic sodes for data download. 
numDays = 3 # how many days to download
lastBusinessClose, isMarketOpen  = data.getLastBusinessDate()
start = lastBusinessClose - timedelta(days=numDays)
print (f"Last Close Business: {lastBusinessClose}")

# this will download till last business day (regardless when it is run during the day)
end = datetime.today().date()   
print (f"Start {start} , End {end} ||  datetime.today().date()")
yf.download(tickers='SPY', interval='1h', start=start, end=end,  group_by="Ticker").tail(5)

# this will download till last tick current day if market it open
end = datetime.today().date()  + timedelta(days=1)
print (f"Start {start} , End {end} || datetime.today().date()  + timedelta(days=1)")
yf.download(tickers='SPY', interval='1h', start=start, end=end,  group_by="Ticker").tail(5)

# this will download till 2nd last close of business (useless)> yahoo downloads till end-1 day
end = lastBusinessClose
print (f"Start {start} , End {end} || lastBusinessClose")
yf.download(tickers='SPY', interval='1h', start=start, end=end,  group_by="Ticker").tail(5)

### the main logic to define end date : pre market, during open market and post market 

# add check: if open: download till last business if closed else download till tomorrow
lastBusiness, isMarketOpen = data.getLastBusinessDate()
if isMarketOpen :
    # end is (yesterday) last business: for yfinance its today()
    end = datetime.today().date() 

else : # if market is closed both pre and post 
    # end is day+1 (tomorrow) : today() + 1
    end = datetime.today().date() + timedelta(days=1)

print ( start, end )
yf.download(tickers='SPY', interval='1h', period = '1d', start=start, end=end, group_by="Ticker")

## Other checks : use of kwarg `period` to bypass (start, end) hassle 
yf.download(tickers='AMD', interval='1d', period='1d', group_by="Ticker") #, prepost=True)
yf.download(tickers='AMD', interval='1h', period='1d', group_by="Ticker") #, prepost=True)
yf.download(tickers='AMD', interval='30m', period='1d', group_by="Ticker") #, prepost=True)

## period will bypass end unless start is also mentioned ! important 
datetime.today().date() - timedelta(days=1)
yf.download(tickers='AMD', interval='1h', period='730d', group_by="Ticker") #, prepost=True)
yf.download(tickers='AMD', interval='5m', period='60d', group_by="Ticker") #, prepost=True)

## both start, end if present then will bypass period 
yf.download(tickers='SPY', interval='1h', period = '5d', start=None, end=None, group_by="Ticker")
yf.download(tickers='SPY', interval='5m', period = '1d', start=None, end=None, group_by="Ticker")


## end main logic 

##################   END Yahoo API behavior  ##################


# ##  Agenda
# force Update to max allowed download limits 
# Update Daily close to [1H, 5m] close
# remove after and pre hours is any (need to think how to do this)  
# remove duplicates Resort database by index    


# auto reload modules for notebook 
%load_ext autoreload
%autoreload 2

pp = data.forceUpdateDataAll(numdays=None, watchlistName="WatchListLive.pickle",persist=False)

pp = data.forceUpdateData(numdays=None, watchlistName="WatchListLive.pickle", interval='5m')