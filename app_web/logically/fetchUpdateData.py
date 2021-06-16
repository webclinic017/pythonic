import os
import queue
import time
from datetime import date, datetime, timedelta

import finta as ft
import numpy as np
import pandas as pd
import pandas_ta as ta
import yfinance as yf

import algo1

import genericProcessConsumerPool  as processThread # # communicate using q

# Source for data PICKLES 

TICKDATA    = '/home/towshif/code/python/pythonic/database/data/'
ALGODATA    = '/home/towshif/code/python/pythonic/database/dataAlgo/'
RESULTS     = '/home/towshif/code/python/pythonic/database/dataResults/'
DATAROOT    = '/home/towshif/code/python/pythonic/database/' 
OLDDATA     = '/home/towshif/code/python/pythonic/database/olddata/' 
DATATEMP     = '/home/towshif/code/python/pythonic/database/dataTemp/' 



# read watchlist 
watchlist = "WatchListLive.pickle"  # initialize 

dfdata = pd.read_pickle(DATAROOT + watchlist ) # read file
# dfdata.to_pickle(DATAROOT+'WatchListLive.pickle') # save file 

# dfdata
symbols = dfdata.TICK.to_list()


download = pd.read_pickle(DATATEMP+'download.pickle') # read file
# print ('Starting Download........')
# download = yf.download(tickers=symbols, interval="60m", period="60d", group_by="Ticker")
# download.to_pickle(DATATEMP+'download.pickle') # save temp download df
## Memory usage 
download.info(verbose=False, memory_usage="deep")
# fix_timezone(download)

# ## troubleshoot -> some symbols delisted will have smaller length - remove them 
# for symbol in symbols: 
#     df = download[symbol].dropna()
#     print (f"{symbol} \t {df.size}") # will print symbol and length of its DF 


p = download['QQQ']
# download=download.dropna() # do not drop na on level 0 df 

# df = getData (symbol='AMD', interval='1H')
# download['AMD']


def compute (df,i,k) : # simulate a high compute or low latency IO process   
    
    tic = time.perf_counter()
    
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

    toc = time.perf_counter()    
    print (f"Compute {i} done in {toc - tic:0.4f} secs")
    # print (f"Compute {i} done in {k} secs")



# ## troubleshoot -> some symbols delisted will have smaller length - remove them 
# tic = time.perf_counter()
# for symbol in symbols: 
#     df = download[symbol].dropna()
    
#     compute (df,symbol,10)
#     # package = compute, (df, symbol, 10), symbol+" compute"
#     # q.put (package)  # format: (func, (*args), jobName)
#     # has_q.release()

# toc = time.perf_counter()
# print (f"Finished in  {toc - tic:0.4f} seconds")
# # q.qsize()


## troubleshoot -> some symbols delisted will have smaller length - remove them 


##########################  Simple Compute test ##############
# for symbol in symbols: 
#     df = download[symbol].dropna()
#     df = df.copy()   
#     # compute (df,symbol,10)
#     package = compute, (df, symbol, 10), symbol+" compute"

#     processThread.putQ (package)  # format: (func, (*args), jobName) to queue a process job 
##############################################################



##########################  Simple Compute test ##############

# processThread.max_workers = 20  # Set Global thread count 
# processThread.setMaxWorker(30)
processThread.initialize(8)

for symbol in symbols: 
    df = download[symbol].dropna()
    df = df.copy()  
    # compute (df,symbol,10)  ## Sequential run - no threads
    # package = compute, (df, symbol, 10), symbol+" compute"

    # import algo1 # this processing takes ~ 56.4819 seconds for 103 images + indicator and 
    package = algo1.AlgoImage2, (df, symbol, '1H', (-201,None), False, False, False), symbol+" compute"
    
    processThread.putQ (package)  # format: (func, (*args), jobName) to queue a process job 

# time.sleep(25)
# processThread.endQ() # exit all threads 

##############################################################



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



def getData (symbol='^GSPC', interval='1H', dates=None, bars=None, period=None, days=None) : # only 1 symbol ata a time # download if does not exist 

    flink = TICKDATA + symbol+'.'+interval+'.pickle'
    dfdata = None
    if not os.path.exists(flink) : # then download an save it 
        # correct interval text alternatives 
        finterval = {
            "1H": "60m",
            "1h": "60m",
            "H1": "60m",
            "h1": "60m",
            "1D": "1d",
            "1d": "1d",
            "5m": "5m",
            "5M": "5m",
        }
        interval = finterval.get(interval, None)
        if interval == None : return None

        dfdata = yf.download(tickers=symbol, interval=interval, period="730d")
        if len(dfdata)>0  : # if successful download     
            pd.to_pickle(dfdata, flink)
            print ("Successful download : ", symbol, interval)
            # print (dfdata.head(10))            
        else : 
            print (symbol, 'ERROR!')
            # exit loop 
    else : # read from pickle 
        dfdata = pd.read_pickle(flink)
    df = dfdata

    if not dates == None : # only
        sd, ed = dates
        df = dfdata.loc[sd:ed]
    elif not bars == None: # only
        sb, eb = bars
        print (bars)
        df = df.iloc[sb:eb]

    return df


def getLiveData (symbol='^GSPC', interval='1H', dates=None, bars=None, period=None) : # only 1 symbol ata a time # download if does not exist 

    dfdata = None
    # correct interval text alternatives 
    finterval = {
        "1H": "60m",
        "1h": "60m",
        "H1": "60m",
        "h1": "60m",
        "1D": "1d",
        "1d": "1d",
        "5m": "5m",
        "5M": "5m",
    }
    interval = finterval.get(interval, None)
    if interval == None : return None


    if not period == None: 
        dfdata = yf.download(tickers=symbol, interval=interval, period=period)
    else: 
        return 'Period Not specified'
    
    if len(dfdata)>0  : # if successful download             
        print ("Successful download : ", symbol, interval, period)
        # print (dfdata.head(10))            
    else : 
        print (symbol, 'ERROR!')
        # exit loop 

    df = dfdata

    # filter operations 
    if not dates == None : # only
        sd, ed = dates
        df = dfdata.loc[sd:ed]
    elif not bars == None: # only
        sb, eb = bars
        print (bars)
        df = df.iloc[sb:eb]

    return df
