import datetime as dt
import random as rnd
from datetime import date, datetime, time, timedelta

import matplotlib.pyplot as plt
import mplfinance as mpf
import numpy as np
import pandas as pd
import pandas_ta as ta
import yfinance as yf

# %load_ext autoreload
# %autoreload 2

from TTM_Chart import Chart

# Read this : pandas_ta and examples 
# https://github.com/twopirllc/pandas-ta/blob/master/examples/example.ipynb
# 

# Initialization
# price_size = (16, 8)
# ind_size = (16, 3.25)
# # All Data: 0, Last Four Years: 0.25, Last Two Years: 0.5, This Year: 1, Last Half Year: 2, Last Quarter: 3
# yearly_divisor = 1
# recent = int(ta.RATE["TRADING_DAYS_PER_YEAR"] / yearly_divisor) if yearly_divisor > 0 else df.shape[0]
# print(recent)
def recent_bars(df, tf: str = "1y"):
    # All Data: 0, Last Four Years: 0.25, Last Two Years: 0.5, This Year: 1, Last Half Year: 2, Last Quarter: 4
    yearly_divisor = {"all": 0, "10y": 0.1, "5y": 0.2, "4y": 0.25, "3y": 1./3, "2y": 0.5, "1y": 1, "6mo": 2, "3mo": 4}
    yd = yearly_divisor[tf] if tf in yearly_divisor.keys() else 0
    return int(ta.RATE["TRADING_DAYS_PER_YEAR"] / yd) if yd > 0 else df.shape[0]


symbol = 'AMD'
sd = datetime(2020, 8, 1)
ed = datetime(2021, 2, 26)

df = yf.download(tickers=symbol, start=sd, end=ed, interval="1d")
# df = yf.download(tickers=symbol, start=sd, end=ed, interval="30m")
# df = yf.download(tickers=symbol, start=sd, end=ed, interval="15m")
# df = yf.download(tickers=symbol, start=sd, end=ed, interval="5m")
# df = yf.download(tickers=symbol, start=sd, end=ed, interval="5m", prepost=True)
# df = yf.download(tickers=symbol, start=sd, end=ed, interval="15m", prepost=True)

# cdf = squeeze(df)
# chart(cdf)

# Chart(df, style="yahoo", title="TEST", verbose=False,
#     last=recent_bars(df), rpad=10, clr=True, squeeze=True,
#     show_nontrading=False, # Intraday use if needed
# )
