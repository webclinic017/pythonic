"""
Script to check last updated values in database randomly.
"""
import pandas as pd
import app_web.logically.datasource as data
import random
import os.path, time
import sys

# get all the arguments from commandline
list_of_arguments = sys.argv

symbol = None

## if symbol provided in arg use that else select a random symbol from watchlist
if len(list_of_arguments) > 1 :
    symbol = list_of_arguments[1]
    print(f"Symbol: {list_of_arguments[1]}")
else:
    # load a watchlist
    wl = data.getWatchlist(verbose=True) # load default watchlist
    symbols = wl.index.tolist()
    symbol=random.choice(symbols) # select a symbol randomly from list of symbols
    print ("Symbol:",symbol, " (Random from watchlist)" )


print ("Timeframe : 1D")
d = data.updateDataEOD(interval='1D', persist=False)
print (d)

print ("Timeframe : 1H")
d = data.updateDataEOD(interval='1H', persist=False)
print (d)

print ("Timeframe : 5m")
d = data.updateDataEOD(interval='5m', persist=False)
print (d)

# print ("**** Last Modified date ****")
fname = "/home/towshif/code/python/pythonic/database/data/SPY.1H.pickle"
print("Last modified: %s" % time.ctime(os.path.getmtime(fname)))
# print("Created: %s" % time.ctime(os.path.getctime(fname)))
print ()



# # test

# symbols = ['SPT', 'LB', 'SPY', 'MPC', 'MAR', 'MMC', 'MLM', 'MAS', 'MA', 'MAT', 'MKC', 'MCD', 'MCK', 'MDT', 'MRK', 'MRO', 'M', 'MAC', 'MTB', 'LYB', 'L', 'LMT', 'LKQ', 'LNC', 'LLY', 'LEG', 'LH', 'KR', 'KHC', 'KSS', 'KMI', 'MET', 'MTD', 'MGM', 'MCHP', 'NUE', 'NRG', 'NCLH', 'NOC', 'NTRS', 'NSC', 'JWN', 'NI', 'NKE', 'NLSN', 'NEE', 'NWS', 'NWSA', 'NEM', 'NWL', 'NTAP', 'NAVI', 'NOV', 'NDAQ', 'MSI', 'MOS', 'MS', 'MCO', 'MNST', 'MON', 'MDLZ', 'TAP', 'MHK', 'MAA', 'KIM', 'KMB', 'KEY', 'K', 'HPE', 'HES', 'HSY', 'HSIC', 'HP', 'HCA', 'HAS', 'HIG', 'HOG', 'HBI', 'HAL', 'GWW', 'GT', 'GS', 'GPN', 'GILD', 'GPC', 'GM', 'GIS', 'GE', 'GD', 'IT', 'GRMN', 'GPS', 'FCX', 'BEN', 'FBHS', 'FTV', 'F', 'HLT', 'ORLY', 'HOLX']

# import yfinance as yf
# import pandas as pd

# yf.download(tickers=symbols, interval='1D', period='200d', group_by="Ticker")
