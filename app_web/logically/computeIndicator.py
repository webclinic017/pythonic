#   computeIndicator.py
##  - All common indicators, 
#   - Special indicators
#   - Stop functions    : 
#   - Targets:          : Auto FIB  


import finta as ft
import numpy as np
import pandas as pd
import pandas_ta as ta
import yfinance as yf
from time import sleep
from genericProcessConsumerPool import * # # communicate using q
import dfutils as dutil 

Algoddr = {}
process_counter=0

has_algoq = Semaphore(value=0)
has_process = Semaphore(value=0)

def call_back(data):  # return from process pool
    symbol = None 
    interval = None 

    if data is not None: 
        df, symbol, interval = data    
        Algoddr[symbol] = df    
    else: 
        print ("Algo expection occured in process pool. check logs.")
    
    # print (f"Completed {symbol} {interval}")

    # has_algoq.acquire()

    # if (process_counter == 0): 
    #     has_process.release() # release main thread lock 

    # Add to Queue # etc etc 


# # initialize process pool compute threads 
initialized = False
# initialize_processPool(25) # 20 process threads
def endCompute() :     
    global initialized
    if initialized: 
        endQ() # do not double queue endQ
        initialized = False 
    else: 
        print ("Warn: Compute Nodes already terminated.")


# Parallel Compute : MultiProcessing 
def compute_all (ddr=None, symbols=None, interval=None) :
    global initialized
    if not initialized : 
        initialize_processPool(25) # 20 process threads
        initialized = True

    global Algoddr
    Algoddr = {} # reset local algodf to a `new` empty dict
    
    print (f"Revceived {ddr.keys()} \nDict Count ={len(ddr)}")
    
    setProcessLock (has_process) # set the semaphore to consumer. 
    # has_algoq.release()

    for symbol, dfdata in ddr.items() : 

        # dfdata = df.copy()
        # print (f"{symbol} found ")
        package = compute_indicatorsA, (dfdata, symbol, interval), symbol+" compute", call_back
        putQ (package)  # format: (func, (*args), jobName)
        # has_algoq.release()

    print (f"Locking thread. [ Compute process count {len(ddr)} ]" )

    while has_process.acquire():  # lock thread until complete execution 
        break 

    text = f"\nCompute Queue Process Complete. \nUnlocked thread. => QSIZE: {processQ.qsize()} "
    # print (text)
    dutil.printInColor(text)

    print (f"AlgoDF Count {len(Algoddr)} | interval {interval} \n{Algoddr.keys()}")
    if len(Algoddr) ==0 : 
        dutil.printWarning(f"Some Error occurred. Algo count is Zero.")
    #     sleep(1)
    # #     # has_algoq.release()
    # #     print ("QSize", processQ.qsize())
    
    # # # sleep (2)
    # print ("QSize is zero. ==> Returning... to main thread")
    # # # putQ("END") # kill the processPool 
    
    return Algoddr


# Sequencial compute 
def compute_all_seq (ddr=None, symbols=None, verbose=False) :
    tic = time.perf_counter()
    
    inDict = {}
    for symbol, dfdata in ddr.items() :
        inDict[symbol] = compute_indicatorsA(dfdata, 1, 0)    
    
    if verbose: 
        toc = time.perf_counter()
        print (f"Compute Time :: {toc - tic:0.4f} seconds")
    return inDict



def compute_indicatorsA (df, symbol, interval, verbose=False) : # simulate a high compute or low latency IO process
    """ Comprises of common compute items 
        1. basic indicators calculations
        2. indicator settings per (stock, timeframe) // not implemented yet
    """
    # print (f"Compute {i} started with {k} secs")
    # if verbose: # measure start time  
    tic = time.perf_counter()

    #############################   Calculation Start 

    df.ta.ha(append=True) # heikinashi bars

    # add HA_Color to signal -1 0 +1 
    df['HA_color'] = np.where(df.HA_close > df.HA_open, 1, -1)
    
    # ema21HA = df['EMA_21HA'] = ta.ema( df.HA_close, length=21, append=True)
    ema9 = df.ta.ema(length=9, append=True)
    ema21 = df.ta.ema(length=21, append=True)
    ema42 = df.ta.ema(length=42, append=True)
    ema50 = df.ta.ema(length=50, append=True)
    ema100 = df.ta.ema(length=100, append=True)
    ema150 = df.ta.ema(length=150, append=True)
    keltner = df.ta.kc(append=True)
    squeezes = df.ta.squeeze(lazybear=False, detailed=True, append=True) 
    # squeezes = df.ta.squeeze(lazybear=True, detailed=True, append=True) # _LB
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

    # add HA_Color to signal -1 0 +1 
    # df['signal_trHAcolor'] = df['HA_color']

    # define stack EMA Extreme:base=9 ::  +1: positive bullish, 0:undecided, -1:negative bearish
    df['signal_StackEMA'] = np.where(
        (df.EMA_9 > df.EMA_21) & 
        (df.EMA_21 > df.EMA_50) & 
        (df.EMA_50 > df.EMA_100) &
        (df.EMA_100 > df.EMA_150)      
        ,1, np.where(
        (df.EMA_9 < df.EMA_21) & 
        (df.EMA_21 < df.EMA_50) & 
        (df.EMA_50 < df.EMA_100) &
        (df.EMA_100 < df.EMA_150), -1, 0))

    # define stack EMA Softer:base=21 :: +1: positive bullish, 0:undecided, -1:negative bearish
    df['signal_StackEMA21'] = np.where(
        # (df.EMA_9 > df.EMA_21) & 
        (df.EMA_21 > df.EMA_50) & 
        (df.EMA_50 > df.EMA_100) &
        (df.EMA_100 > df.EMA_150)      
        ,1, np.where(
        # (df.EMA_9 < df.EMA_21) & 
        (df.EMA_21 < df.EMA_50) & 
        (df.EMA_50 < df.EMA_100) &
        (df.EMA_100 < df.EMA_150), -1, 0))

    # reformat Squeese (Original) for Charting 
    df['SQZ'] = df['SQZ_ON']    # final SQZ market
    # df['SQZ_Hist'] = df['SQZ_20_2.0_20_1.5_LB'] # final SQZ Hist
    df['SQZ_Hist'] = df['SQZ_20_2.0_20_1.5'] # final SQZ Hist
    # mark increasing decreasing : 2 inc blue, 1 dec deep blue, -1 red dec, -2 yellow inc
    df['SQZ_HistC'] = np.where(df['SQZ_PINC'].notnull(), 2, np.nan)
    df['SQZ_HistC'] = np.where(df['SQZ_PDEC'].notnull(), 1, df['SQZ_HistC'])
    df['SQZ_HistC'] = np.where(df['SQZ_NDEC'].notnull(), -1, df['SQZ_HistC'])
    df['SQZ_HistC'] = np.where(df['SQZ_NINC'].notnull(), -2, df['SQZ_HistC'])

    #############################   Calculation END 

    if verbose: 
        toc = time.perf_counter()
        print (f"Compute Time :: {toc - tic:0.4f} seconds")
        print (f"Compute {symbol} done with {interval} interval.")
    
    return (df, symbol, interval)


# https://www.mikulskibartosz.name/how-to-reduce-memory-usage-in-pandas/
# 70% compression with smaller datatypes

def reduce_mem_usage(df):
    start_mem = df.memory_usage().sum() / 1024**2
    print('Memory usage of dataframe is {:.2f} MB'.format(start_mem))
    
    for col in df.columns:
        col_type = df[col].dtype
        
        if col_type != object:
            c_min = df[col].min()
            c_max = df[col].max()
            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)  
            else:
                if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                    df[col] = df[col].astype(np.float16)
                elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float64)
        else:
            df[col] = df[col].astype('category')

    end_mem = df.memory_usage().sum() / 1024**2
    print('Memory usage after optimization is: {:.2f} MB'.format(end_mem))
    print('Decreased by {:.1f}%'.format(100 * (start_mem - end_mem) / start_mem))
    
    return df