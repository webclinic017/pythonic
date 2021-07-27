"""
Script to check last updated values in database randomly.
"""
import pandas as pd
import app_web.logically.datasource as data
import random

# load a watchlist
wl = data.getWatchlist() # load default watchlist
symbols = wl.index.tolist()
symbol=random.choice(symbols)
print ("Symbol:",symbol )


print ("Timeframe : 1D")
d = data.getDataFromPickle(symbol, interval='1D').tail(5)
c1D = d.iloc[-1].Close
print (d)

print ("Timeframe : 4H")
d = data.getDataFromPickle(symbol, interval='4H').tail(5)
c4H = d.iloc[-1].Close
print (d)

print ("Timeframe : 1H")
d = data.getDataFromPickle(symbol, interval='1H').tail(5)
c1H = d.iloc[-1].Close
print (d)

print ("Timeframe : 5m")
d = data.getDataFromPickle(symbol, interval='5m').tail(5)
c5m = d.iloc[-1].Close
print (d)

print ("**** Comparing Close Data ****")
print ('Close [1D, 4H, 1H, 5m]:', c1D, c4H, c1H, c5m )
