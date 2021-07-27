"""
Script to check last updated values in database randomly.
"""
import pandas as pd
import app_web.logically.datasource as data
import random
import os.path, time

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
print (f'Close [\n1D : {c1D}\n4H : {c4H}\n1H : {c1H}\n5m : {c5m}]')

# print ("**** Last Modified date ****")
fname = "/home/towshif/code/python/pythonic/database/data/SPY.1H.pickle"
print("Last modified: %s" % time.ctime(os.path.getmtime(fname)))
# print("Created: %s" % time.ctime(os.path.getctime(fname)))
print ()

