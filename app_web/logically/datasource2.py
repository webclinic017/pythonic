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


def getData (symbol='SPY', interval='1H', dates=None, bars=None, period=None, days=None) : # only 1 symbol ata a time # download if does not exist 
    
    # correct interval text alternatives for pickle names
    finterval = {
        "1H": "1H",
        "1h": "1H",
        "H1": "1H",
        "h1": "1H",
        "1D": "1D",
        "1d": "1D",
        "d1": "1D",
        "D1": "1D",
        "5m": "5m",
        "5M": "5m",        
    }
    interval = finterval.get(interval, None)
    if interval == None : return None

    # generate the link to piclke file 
    flink = TICKDATA + symbol+'.'+interval+'.pickle'
    # print (flink) # debug 

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
            "d1": "1d",
            "5m": "5m",
            "5M": "5m",        
        }
        interval = finterval.get(interval, None)
        if interval == None : return None

        dfdata = yf.download(tickers=symbol, interval=interval, period="730d")
        if len(dfdata)>0  : # if successful download 
            # fix timezone 
            dfdata = fix_timezone(dfdata)                
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
        "d1": "1d",
        "D1": "1d",
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


def getWatchlist (watchlistName=None, interval='1H') : 
    symbols = None 

    if not watchlistName : 
        # read default watchlist 
        # read watchlist
        watchlistName = "WatchListDB.pickle"  # initialize

    watchlist = pd.read_pickle(DATAROOT + watchlistName ) # read file
    return watchlist    


def loadDatatoMemory (watchlistName=None, interval='1H') : 
    symbols = None 

    if not watchlistName : 
        # read default watchlist 
        # read watchlist
        watchlistName = "WatchListDB.pickle"  # initialize

    watchlist = pd.read_pickle(DATAROOT + watchlistName ) # read file    
    symbols = watchlist.TICK.to_list()
    
    ddr = {} # define empty 
    for symbol in symbols:  # load all data to memory 
        ddr[symbol] = getData (symbol=symbol, interval=interval).dropna()
    
    return ddr, symbols 

def updateDataEOD (watchlistName=None, interval=None, persist=False) : 
    """ Update database end of day (EOD) data for 
        default (all): 1H, 1D, 4H, 5m intervals unless specified
        persists (to disk) : False (default)
    """
    symbols = None 

    if not watchlistName : 
        # read default watchlist 
        # read watchlist
        watchlistName = "WatchListDB.pickle"  # initialize

    watchlist = pd.read_pickle(DATAROOT + watchlistName ) # read file    
    symbols = watchlist.TICK.to_list()

## Helper 
def updateWatchlistLastUpdated(watchlistName=None, interval=None) : 
    """ Update watchlists with lastupdated column for interval : 1H, 1D, 4H, 5m  
        column name format: start.<interval> 
    """
    if not watchlistName : 
        # read default watchlist 
        # read watchlist
        watchlistName = "WatchListDB.pickle"  # initialize

    watchlist = pd.read_pickle(DATAROOT + watchlistName ) # read file    
    watchlist['id'] = watchlist['TICK']
    watchlist.set_index('id', inplace=True)  # prevent duplicates 

    symbols = watchlist.TICK.to_list()
    # print ('symbols: ', symbols)

    if not interval : # when not specified default = all     
        for interval in ['1H', '1D', '5m'] : 
            for symbol in symbols:  # load all data to memory 
                d = getData (symbol=symbol, interval=interval).dropna()
                start = d.index[0] # first datetime index 
                end = d.index[-1] # last datetime index 
                watchlist.loc[symbol, ['start.' + interval, 'end.' +interval]] = [start, end]  # update start and end time 
    #  Save watchlist to disk 
    watchlist.to_pickle(DATAROOT+watchlistName)
    print (f"Successfully updated and saved watchlist {watchlistName} to disk")

    return watchlist  


def fix_timezone (dfdata) : # for a single DF : dfdata
    """Timezone/ daylight saving fix for US instruments: 
        get rid of -4:00 NY time added text 
    """
    notfound = []
    dfdata['Datetime'] = dfdata.index
    dfdata['Datetime'] = dfdata['Datetime'].dt.tz_localize(None)
    dfdata.set_index('Datetime', inplace=True)

    return dfdata

    


