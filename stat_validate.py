"""
Script to Validate entire database.
Includes repetitions and extended hours.
Expected values. 
"""

import pandas as pd
from datetime import date
import app_web.logically.datasource as data
# import datasource as data
import random
import sys, os.path, time

# get all the arguments from commandline
list_of_arguments = sys.argv

symbol = None

## if symbol provided in arg use that else select a random symbol from watchlist
if len(list_of_arguments) > 1 :
    symbol = list_of_arguments[1]
    print(f"Symbol: {list_of_arguments[1]}")

else:
    print("*** No Argument provided. Pass Symbol as arg : stat_validate.py SPY")
    # load a watchlist
    wl = data.getWatchlist(verbose=True) # load default watchlist
    symbols = wl.index.tolist()
    symbol=random.choice(symbols) # select a symbol randomly from list of symbols
    print ("Symbol:",symbol, " (Random from watchlist)" )



## following define # entries per day
cinterval = {
    "1D"    : 1,
    "1d"    : 1,
    "1h"    : 7,
    "1H"    : 7,
    "4H"    : 2,
    "4h"    : 2,
    "5m"    : 78,
}


### check for data consistency
#watchlist = data.getWatchlist('WatchListLive.pickle') # defaults to default watchlist
#symbolslist = watchlist.TICK.to_list()
# len(symbolslist)

print ("\n*************     DATA HEALTH ANALYSIS        ****************")

for interval in  ['1D', '1H', '5m'] :
    print ("\n#############")
    print (f"{interval} Analysis ::	{symbol}")
    # print ("Expected count/day = ", cinterval.get(interval, None)) # expected count

    dfdata = data.getDataFromPickle(symbol=symbol, interval=interval) # read
    if dfdata is None : exit(0) 

    outlierData = data.dataConsistencyCheck(dfdata, interval, verbose=True).loc[str(date.today().year):]

    if len(outlierData) >0 : 
        print ("Current Year: ", len(outlierData))

    # print (outlierData)
    # print ("Outliers\n", outlierData)

    # print (outlierlist)


# outlierData.iloc[-1:].index[0].strftime("%m/%d/%y %H:%M")

## Debug
# date.today().year
# symbol='^GSPC'
# interval='1H'
# dfdata = data.getDataFromPickle(symbol=symbol, interval=interval) # read
# outlierData = data.dataConsistencyCheck(dfdata, interval, returns=True).loc['2021':



# # test 

# symbols = ['SPT', 'LB', 'SPY', 'MPC', 'MAR', 'MMC', 'MLM', 'MAS', 'MA', 'MAT', 'MKC', 'MCD', 'MCK', 'MDT', 'MRK', 'MRO', 'M', 'MAC', 'MTB', 'LYB', 'L', 'LMT', 'LKQ', 'LNC', 'LLY', 'LEG', 'LH', 'KR', 'KHC', 'KSS', 'KMI', 'MET', 'MTD', 'MGM', 'MCHP', 'NUE', 'NRG', 'NCLH', 'NOC', 'NTRS', 'NSC', 'JWN', 'NI', 'NKE', 'NLSN', 'NEE', 'NWS', 'NWSA', 'NEM', 'NWL', 'NTAP', 'NAVI', 'NOV', 'NDAQ', 'MSI', 'MOS', 'MS', 'MCO', 'MNST', 'MON', 'MDLZ', 'TAP', 'MHK', 'MAA', 'KIM', 'KMB', 'KEY', 'K', 'HPE', 'HES', 'HSY', 'HSIC', 'HP', 'HCA', 'HAS', 'HIG', 'HOG', 'HBI', 'HAL', 'GWW', 'GT', 'GS', 'GPN', 'GILD', 'GPC', 'GM', 'GIS', 'GE', 'GD', 'IT', 'GRMN', 'GPS', 'FCX', 'BEN', 'FBHS', 'FTV', 'F', 'HLT', 'ORLY', 'HOLX']

# import yfinance as yf
# import pandas as pd

# yf.download(tickers=symbols, interval='1D', period='200d', group_by="Ticker")
