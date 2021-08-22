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

# data.force_sort_index_all(persist=True)


### check for data consistency
watchlist = data.getWatchlist('WatchListLive.pickle') # defaults to default watclist
symbolslist = watchlist.TICK.to_list()
# len(symbolslist)

print ("\n*************     DATA HEALTH ANALYSIS        ****************")

for interval in  ['1D', '1H', '5m', '4h'] : 
    outlierlist = []
    for symbol in symbolslist:
        dfdata = data.getDataFromPickle(symbol=symbol, interval=interval) # read 

        outlierData = data.dataConsistencyCheck(dfdata, interval, verbose=False).loc[str(date.today().year):]
        if len(outlierData) >0 : outlierlist.append(symbol)
    
    print ("\n#############")
    print (f"{interval} Analysis ::::  Found {len(outlierlist)} outliers")
    print (outlierlist)

## Debug 
# date.today().year   
# symbol='^GSPC'
# interval='1H'
# dfdata = data.getDataFromPickle(symbol=symbol, interval=interval) # read 
# outlierData = data.dataConsistencyCheck(dfdata, interval, returns=True).loc['2021':]



# # test 

# symbols = ['SPT', 'LB', 'SPY', 'MPC', 'MAR', 'MMC', 'MLM', 'MAS', 'MA', 'MAT', 'MKC', 'MCD', 'MCK', 'MDT', 'MRK', 'MRO', 'M', 'MAC', 'MTB', 'LYB', 'L', 'LMT', 'LKQ', 'LNC', 'LLY', 'LEG', 'LH', 'KR', 'KHC', 'KSS', 'KMI', 'MET', 'MTD', 'MGM', 'MCHP', 'NUE', 'NRG', 'NCLH', 'NOC', 'NTRS', 'NSC', 'JWN', 'NI', 'NKE', 'NLSN', 'NEE', 'NWS', 'NWSA', 'NEM', 'NWL', 'NTAP', 'NAVI', 'NOV', 'NDAQ', 'MSI', 'MOS', 'MS', 'MCO', 'MNST', 'MON', 'MDLZ', 'TAP', 'MHK', 'MAA', 'KIM', 'KMB', 'KEY', 'K', 'HPE', 'HES', 'HSY', 'HSIC', 'HP', 'HCA', 'HAS', 'HIG', 'HOG', 'HBI', 'HAL', 'GWW', 'GT', 'GS', 'GPN', 'GILD', 'GPC', 'GM', 'GIS', 'GE', 'GD', 'IT', 'GRMN', 'GPS', 'FCX', 'BEN', 'FBHS', 'FTV', 'F', 'HLT', 'ORLY', 'HOLX']

# import yfinance as yf
# import pandas as pd

# yf.download(tickers=symbols, interval='1D', period='200d', group_by="Ticker")