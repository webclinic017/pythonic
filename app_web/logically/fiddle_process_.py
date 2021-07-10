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

ddr1D  = {}
ddr4H  = {}
ddr1H  = {}
Addr1D = {}
Addr4H = {}
Addr1H = {}


ddr1D, symbols = data.loadDatatoMemory(interval='1D', filter=75)
ddr4H, symbols = data.loadDatatoMemory(interval='4H', filter=10)
ddr1H, symbols = data.loadDatatoMemory(interval='1H', filter=75)

symbols

Addr4H = compute_all(ddr=ddr4H, symbols=symbols, interval='4H')
print ("Compute Done 4H.....")
# Addr1H = compute_all(ddr=ddr1H, symbols=symbols, interval='1H')
# print ("Compute Done 1H.....")
# Addr1D = compute_all(ddr=ddr1D, symbols=symbols, interval='1D')
# print ("Compute Done 1D.....")



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





###############         IPYTHON  SHELL      ##################
# start a python debug shell and embed to application 
# read: https://stackoverflow.com/questions/66121284/ipython-repl-anywhere-how-to-share-application-context-with-ipython-console-for

import ipdb
from IPython import embed

ipdb.set_trace()
# ipdb.set_trace()

# ipdb> from IPython import embed
# ipdb> embed()
###############################################################



############ Advanced Problems 

# orphaned Nodes Problem (sample output )
"""
    25
    Generic consumer: Threads started ......
    Staring CPU bound tasks with 25 process workers.Revceived dict_keys(['SPY', 'SPXU', 'SPXS', 'JNUG', 'AAL', 'WGO', 'DAL', 'AAPL', 'AMAT', 'AMD']) 
    `Dict Count =10`

    Locking thread. [ Compute process count 10 ]
    Finished in  3.8621 seconds
    Waiting for Queue ......

    Compute Queue Process Complete. 
    Unlocked thread. => QSIZE: 0 
    `AlgoDF Count 9` | interval 4H 
    [12]


    Addr4H = compute_all(ddr=ddr4H.copy(), symbols=symbols, interval='4H')
    Revceived dict_keys(['SPY', 'SPXU', 'SPXS', 'JNUG', 'AAL', 'WGO', 'DAL', 'AAPL', 'AMAT', 'AMD']) 
    Dict Count =10
    Locking thread. [ Compute process count 10 ]

    Compute Queue Process Complete. 
    Unlocked thread. => QSIZE: 0 
    AlgoDF Count 0 | interval 4H 
    Some Error occurred. Algo count is Zero.

"""