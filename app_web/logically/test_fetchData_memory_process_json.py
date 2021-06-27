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

# symbols = ['SPY', 'SPXU', 'SPXS', 'JNUG', 'AAL', 'WGO', 'DAL', 'AAPL', 'AMAT', 'AMD', 'AMZN', 'BA', 'BAC', 'CLX', 'COST', 'DIS', 'FB', 'GOOG', 'INTC', 'IVV', 'KLAC', 'LRCX', 'MRNA', 'MSFT', 'MU', 'NFLX', 'NVDA', 'ONEQ', 'PTON', 'QQQ', 'SAIA', 'SBUX', 'SKX', 'SPCE', 'TSLA', 'UAL', 'URI', 'VDE', 'ZM', 'LPX', 'SNBR', 'UCTT', 'WSM', 'APPS', 'HZO', 'WAL', 'COWN', 'DHI', 'ARCB', 'UFPI', 'LGIH', 'AMAT', 'THI', 'ABG', 'CTB', 'KIRK', 'LAD', 'TFII', 'LOB', 'TPX', 'USAK', 'CENTA', 'LEN', 'LOW', 'SYNA', 'TBBK', 'WGO', 'CALX', 'GSL', 'KLIC', 'AVNW', 'HZNP', 'AMRK', 'BGFV', 'CCS', 'GROW', 'HIBB', 'IDT', 'KBH', 'MDC', 'MHO', 'SCVL', 'SLM', 'UNFI', 'ACLS', 'AOUT', 'GPI', 'HIMX', 'HTH', 'RCII', 'TRQ', 'CUBI', 'DAC', 'HVT', 'ICHR', 'MIK', 'ODFL', 'OMI', 'AGCO', '^GSPC', '^NDX', '^DJI', '^VIX', ]

# download = pd.read_pickle(DATATEMP+'download.pickle') # read file
#download = yf.download(tickers=symbols, interval="60m", period="60d", group_by="Ticker")
#download.to_pickle(DATATEMP+'download.pickle') # save temp download df
## Memory usage
# download.info(verbose=False, memory_usage="deep")



# ## troubleshoot -> some symbols delisted will have smaller length - remove them
# for symbol in symbols:
#     df = download[symbol].dropna()
#     print (f"{symbol} \t {df.size}") # will print symbol and length of its DF

# fix_timezone(download)

# p = download['QQQ']
# download=download.dropna() # do not drop na on level 0 df

# df = data.getData (symbol='AMD', interval='1H')

ddr = {} # define empty 

for symbol in symbols:  # load all data to memory 
    ddr[symbol] = data.getData (symbol=symbol, interval='1D').dropna()

# ddr['AMZN']
# ddr['AMZN'].info(verbose=False, memory_usage="deep")



def compute (df,i,k) : # simulate a high compute or low latency IO process
    # print (f"Compute {i} started with {k} secs")
    df.ta.ha(append=True) # heikinashi bars
    df['HA_color'] = np.where(df.HA_close > df.HA_open, 1, -1)
    # ema21HA = df['EMA_21HA'] = ta.ema( df.HA_close, length=21, append=True)
    ema9 = df.ta.ema(length=9, append=True)
    ema21 = df.ta.ema(length=21, append=True)
    ema42 = df.ta.ema(length=42, append=True)
    ema50 = df.ta.ema(length=50, append=True)
    ema100 = df.ta.ema(length=100, append=True)
    ema150 = df.ta.ema(length=150, append=True)
    keltner = df.ta.kc(append=True)
    squeezes = df.ta.squeeze(lazybear=True, detailed=True, append=True)
    bollingers = df.ta.bbands(append=True)

    df['signal_SQ2gauss']= ft.TA.SQZMI(df).apply(lambda x: -1 if x else 0)
    df['signal_trTTM'] = df.ta.ttm_trend(append=True)

    # df['signal_decreasing'] = df.ta.decreasing(length=8).apply(lambda x: -1 if x==1 else x)
    # df['signal_increasing'] =df.ta.increasing(length=8)
    # length = 3
    # df['signal_IDClose'] = df.ta.decreasing(close=df.HA_close, length=length, strict=True).apply(lambda x: -1 if x==1 else x) + df.ta.increasing(close=df.HA_close,length=length, strict=True)
    # df['signal_IDhigh'] = df.ta.decreasing(close=df.HA_high, length=length, strict=True).apply(lambda x: -1 if x==1 else x) + df.ta.increasing(close=df.HA_high,length=length, strict=True)

    # Exit Chandelier (based on FINTA)
    chandelier = ft.TA.CHANDELIER(df, long_period=15, short_period=15)
    df['chxLong'], df['chxShort'] = chandelier['Long.'], chandelier['Short.']
    df['chxLong'] = np.where(df['chxLong'] >= df['close'], np.NaN, df['chxLong'])
    df['chxShort']= np.where(df['chxShort'] < df['close'], np.NaN, df['chxShort'])
    df['signal_sChandelier'] = np.where(df['chxShort'] > 0, -1, 1) # first hint of red
    # df['signal_chandelierL'] = np.where(df['chxLong'] > 0, 1, -1)


    # New Squeeze (black dots) : 1 = ON, 0 = OFF (for 'in_squeeze')
    def in_squeeze(df):
        if df['BBL_5_2.0'] > df['KCLe_20_2'] and df['BBU_5_2.0'] < df['KCUe_20_2'] :
            return 1
    def out_squeeze(df):
        if not (df['BBL_5_2.0'] > df['KCLe_20_2'] and df['BBU_5_2.0'] < df['KCUe_20_2']):
            return 1
    df['squeeze_on'] = df.apply(in_squeeze, axis=1)
    df['squeeze_off'] = df.apply(out_squeeze, axis=1)

    # PSAR Stop Reverse (based on pandas_TA)
    psar = df.ta.psar( append=True)
    # print (df)
    print (f"Compute {i} done with {k} secs")

    return df



# ## troubleshoot -> some symbols delisted will have smaller length - remove them
#tic = time.perf_counter()
#for symbol in symbols:
#    df = download[symbol].dropna()

#    compute (df,symbol,10)
    # package = compute, (df, symbol, 10), symbol+" compute"
    # q.put (package)  # format: (func, (*args), jobName)
    # has_q.release()

#toc = time.perf_counter()
#print (f"Finished in  {toc - tic:0.4f} seconds")
# # q.qsize()


## troubleshoot -> some symbols delisted will have smaller length - remove them


# processThread.initialize(21)

for symbol in symbols[:4]:
    df = ddr[symbol]
    # df = df.copy()
    compute (df,symbol,10)
    # package = compute, (df, symbol, 10), symbol+" compute"

    # processThread.putQ (package)  # format: (func, (*args), jobName)

# q.qsize()

ddr['JNUG'].info(verbose=False, memory_usage="deep")
mpfdf = ddr['JNUG']

squeezes = [col for col in mpfdf if col.startswith('SQZ')]
mpfdf[squeezes][-2:].to_json(orient='split', double_precision=2)
mpfdf[['open', 'high', 'low','close']][-10:].to_json(orient='split', double_precision=2)
mpfdf[['open', 'high', 'low','close']][-50:].to_json(orient='columns', double_precision=2, date_unit='s')

import json
from json import encoder
encoder.FLOAT_REPR = lambda o: format(o, '.2f')
json.dumps(js)

def fix_timezone (dfdata) : # multi index 'df'
    # Timezone/ daylight saving fix
    notfound = []
    # symbols = df.columns.levels[0].tolist()  # list of Ticks in the multi index dataframe
    # for symbol in symbols :
        # dfdata = df [symbol]
    dfdata['Datetime'] = dfdata.index
    dfdata['Datetime'] = dfdata['Datetime'].dt.tz_localize(None)
    dfdata.set_index('Datetime', inplace=True)

    if len(dfdata)>0  : # if successful download
        print ("Successful : ")
        # print (dfdata.head(10))
    # else :
        # exit loop
    else :
        print ('ERROR!')
        # notfound.append(symbol)
    # print (notfound)



def fix_timezone2 (df) : # multi index 'df'
    # Timezone/ daylight saving fix
    notfound = []
    symbols = df.columns.levels[0].tolist()  # list of Ticks in the multi index dataframe
    for symbol in symbols :
        dfdata = df [symbol]
        dfdata['Datetime'] = dfdata.index
        dfdata['Datetime'] = dfdata['Datetime'].dt.tz_localize(None)
        dfdata.set_index('Datetime', inplace=True)

        if len(dfdata)>0  : # if successful download
            print ("Successful : ", symbol)
            # print (dfdata.head(10))
        # else :
            # exit loop
        else :
            print (symbol, 'ERROR!')
            notfound.append(symbol)
    print (notfound)

