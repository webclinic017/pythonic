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

# %load_ext autoreload
# %autoreload 2

ddr, symbols = data.loadDatatoMemory(interval='1D') 
ddr['SAIA']
len (ddr)
ddr.keys()

