# This is a test program to measure time required for 
# pickle read and indicator calculations 
# using processThreadConsumer 

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

# Source for data PICKLES

TICKDATA    = '/home/towshif/code/python/pythonic/database/data/'
ALGODATA    = '/home/towshif/code/python/pythonic/database/dataAlgo/'
RESULTS     = '/home/towshif/code/python/pythonic/database/dataResults/'
DATAROOT    = '/home/towshif/code/python/pythonic/database/'
OLDDATA     = '/home/towshif/code/python/pythonic/database/olddata/'
DATATEMP     = '/home/towshif/code/python/pythonic/database/dataTemp/'



# read watchlist
watchlistName = "WatchListDB.pickle"  # initialize
watchlist = pd.read_pickle(DATAROOT + watchlistName ) # read file
# watchlist.to_pickle(DATAROOT+'WatchListLive.pickle') # save file

# watchlist
symbols = watchlist.TICK.to_list()



# import computeIndicator as cp
from computeIndicator import * 

ddr4H = {}
ddr1D = {}
Addr4H = {}
Addr1D = {}


ddr4H, symbols = data.loadDatatoMemory(interval='4H', filter=50)
ddr1D, symbols = data.loadDatatoMemory(interval='1H', filter=50)

symbols

# Addr4H = cp.compute_all(ddr=ddr4H, symbols=symbols, Addr=Addr4H)
# Addr4H = compute_all(ddr=ddr4H, symbols=symbols, interval='4H')
# print ("Compute started 4H..... plplease wait .... ")
Addr1D = compute_all(ddr=ddr1D, symbols=symbols, interval='1H')
print ("Compute started 1D..... plplease wait .... ")


# putQ("SENTINEL")

# compute_indicatorsA(df=ddr4H['SPY'], symbol='SPY', interval='4H')

# processThread.initialize(21)

# for symbol in symbols[:4]:
#     df = ddr[symbol]
#     # df = df.copy()
#     compute (df,symbol,10)

#     # package = compute, (df, symbol, 10), symbol+" compute"
#     # ddr[symbol] = df
#     # processThread.putQ (package)  # format: (func, (*args), jobName)

# processThread.processQ.qsize()

# # q.qsize()
