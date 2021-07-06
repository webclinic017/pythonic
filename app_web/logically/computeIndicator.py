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


def compute_all(ddr=None, symbols=None) :

    inDict = {}
    for symbol, dfdata in ddr.items() :
        inDict[symbol] = compute_indicatorsA(dfdata, 1, 0)

    return inDict


def compute_indicatorsA (df,i,k) : # simulate a high compute or low latency IO process
    """ Comprises of common compute items 
        1. basic indicators calculations
        2. indicator settings per (stock, timeframe)
    """
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

