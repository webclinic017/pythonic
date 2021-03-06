import os
from datetime import date, datetime, time, timedelta

import numpy as np
import pandas as pd
import yfinance as yf
# Source for data PICKLES 

TICKDATA    = '/home/towshif/code/python/pythonic/database/data/'
ALGODATA    = '/home/towshif/code/python/pythonic/database/dataAlgo/'
RESULTS     = '/home/towshif/code/python/pythonic/database/dataResults/'
DATAROOT    = '/home/towshif/code/python/pythonic/database/' 
OLDDATA     = '/home/towshif/code/python/pythonic/database/olddata/' 
DATATEMP     = '/home/towshif/code/python/pythonic/database/dataTemp/'


def getData (symbol='^GSPC', interval='1H', dates=None, bars=None, period=None) : # only 1 symbol ata a time # download if does not exist 

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
            # Timezone/ daylight saving fix 
            dfdata['Datetime'] = dfdata.index
            dfdata['Datetime'] = dfdata['Datetime'].dt.tz_localize(None)
            dfdata.set_index('Datetime', inplace=True)  

            pd.to_pickle(dfdata, flink)
            print ("Successful download : ", symbol, interval)
            # print (dfdata.head(10))            
        else : 
            print (symbol, 'ERROR!')
            # exit loop 
    else : # read from pickle 
        dfdata = pd.read_pickle(flink)
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
        # Timezone/ daylight saving fix 
        dfdata['Datetime'] = dfdata.index
        dfdata['Datetime'] = dfdata['Datetime'].dt.tz_localize(None)
        dfdata.set_index('Datetime', inplace=True)  
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


