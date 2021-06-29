import os
from datetime import datetime, time, timedelta

import numpy as np
import pandas as pd
import yfinance as yf
# Source for data PICKLES 

TICKDATA    = '/home/towshif/code/python/pythonic/database/data/'
ALGODATA    = '/home/towshif/code/python/pythonic/database/dataAlgo/'
RESULTS     = '/home/towshif/code/python/pythonic/database/dataResults/'
DATAROOT    = '/home/towshif/code/python/pythonic/database/' 
OLDDATA     = '/home/towshif/code/python/pythonic/database/olddata/' 

# Constants 
# correct interval text alternatives 
# for download interval limits for yf.download
dinterval = {
    "1H": ("60m", "730d"),
    "1h": ("60m", "730d"),
    "H1": ("60m", "730d"),
    "h1": ("60m", "730d"),
    "1D": ("1d", "10000d"),
    "1d": ("1d", "10000d"),
    "d1": ("1d", "10000d"),
    "5m": ("5m", "60d"),
    "5M": ("5m", "60d"),        
}
# used for file naming conventions 
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


def getData (symbol='SPY', interval='1H', dates=None, bars=None, period=None, days=None) : # only 1 symbol ata a time # download if does not exist 
    
    # correct interval text alternatives for pickle names
    interval = finterval.get(interval, None)
    if interval == None : return None

    # generate the link to piclke file 
    flink = TICKDATA + symbol+'.'+interval+'.pickle'
    # print (flink) # debug 

    dfdata = None
    
    if not os.path.exists(flink) : # then download an save it 
        print (f"Symbol {symbol} not in database. Downloading from internet.")
        
        # correct interval, period for text alternatives for yf.download
        yinterval, yperiod = dinterval.get(interval, None)
        if yinterval == None : return None

        print (f'Started download {symbol} for {yinterval} {yperiod}. ')
        dfdata = yf.download(tickers=symbol, interval=yinterval, period=yperiod)
        if len(dfdata)>0  : # if successful download 
            # fix timezone 
            dfdata = fix_timezone(dfdata)
            dfdata.drop(dfdata[(dfdata.index.hour ==16) & (dfdata.index.minute == 0)].index, inplace=True) if yinterval=='5m' else None ## drop last row if it contains 16:00 hr data with 0 volume for 5m.
            # pd.to_pickle(dfdata, flink)
            print ("Successful download : ", symbol, yinterval)
            # print (dfdata.head(10))            
        else : 
            print (symbol, yinterval, yperiod, 'ERROR!')
            return None
            # exit loop 
            
    else : # read from pickle 
        dfdata = pd.read_pickle(flink)
    
    df = dfdata # if download successful and len(df) > 0 

    if not dates == None : # only
        sd, ed = dates
        df = dfdata.loc[sd:ed]
    elif not bars == None: # only
        sb, eb = bars
        print (bars)
        df = df.iloc[sb:eb]

    return df

def getDataFromPickle (symbol='SPY', interval='1H', dates=None, period=None) : # only 1 symbol ata a time # download if does not exist 
    
    # correct interval text alternatives for pickle names
    interval = finterval.get(interval, None)
    if interval == None : return None

    # generate the link to piclke file 
    flink = TICKDATA + symbol+'.'+interval+'.pickle'
    # print (flink) # debug 

    dfdata = None
    
    if not os.path.exists(flink) : # then download an save it 
        print (f"Symbol {symbol} not in database. Downloading from internet.")
        return None
        # exit loop             
    else : # read from pickle 
        dfdata = pd.read_pickle(flink)
    return dfdata


def downloadData (symbol='SPY', interval='1H', dates=None, bars=None, period=None, days=None) : # only 1 symbol ata a time # download if does not exist 
    
    # correct interval text alternatives for pickle names
    interval = finterval.get(interval, None)
    if interval == None : return None

    # generate the link to pickle file 
    flink = TICKDATA + symbol+'.'+interval+'.pickle'
    # print (flink) # debug 

    dfdata = None
    
    if not os.path.exists(flink) : # then download an save it 
        print (f"Symbol {symbol} not in database. Downloading from internet.")
        
        # correct interval, period for text alternatives for yf.download
        yinterval, yperiod = dinterval.get(interval, None)
        if yinterval == None : return None

        print (f'Started download {symbol} for {yinterval} {yperiod}. ')
        dfdata = yf.download(tickers=symbol, interval=yinterval, period=yperiod)
        if len(dfdata)>0  : # if successful download 
            # fix timezone 
            dfdata = fix_timezone(dfdata)   
            dfdata.drop(dfdata[(dfdata.index.hour ==16) & (dfdata.index.minute == 0)].index, inplace=True) if yinterval=='5m' else None ## drop last row if it contains 16:00 hr data with 0 volume for 5m.

            # pd.to_pickle(dfdata, flink) # save to disk as pickle 
            print ("Successful download : ", symbol, yinterval, yperiod)
            # print (dfdata.head(10))            
        else : 
            print (symbol, yinterval, yperiod, 'ERROR!')            
            return None
            # exit loop 
    
    else : # read from pickle 
        dfdata = pd.read_pickle(flink)
        print ("File already exists.")
        if dfdata.index[-1] < datetime.today() : print (f"Database outdated. Update this symbol: {symbol}")

    df = dfdata if len(dfdata)>0   else None # if download successful and len(df) > 0 

    if not dates == None : # only
        sd, ed = dates
        df = dfdata.loc[sd:ed]
    elif not bars == None: # only
        sb, eb = bars
        print (bars)
        df = df.iloc[sb:eb]

    return df



def updateData (symbol='SPY', interval='1H', dates=None, bars=None, period=None, days=None, watchlistName=None) : 
    # only 1 symbol ata a time # download if does not exist 
    
    watchlist = getWatchlist(watchlistName) # defaults to default watclist 
    symbols = watchlist.TICK.to_list()

    dfdata = getData(symbol=symbol, interval=interval)

    # print (dfdata)
    if dfdata is None: 
        print (f"ERROR fetching symbol: {symbol}. Returned None.")
    
    elif len(dfdata) > 0  : # another check - df is valid and error free.
    
        # end =  pd.Timestamp(dfdata.index[-1]).to_pydatetime() # get last timestamp
        end =  dfdata.index[-1]  # get last timestamp
        
        print (f"End:{end}")
        
        if end.date() < datetime.today().date() : ## Update if data us outdated 
            print ("DB outdated. Update started")

            ######################      DOWNLOAD  module    ###########################

            # correct interval, period for text alternatives for yf.download
            yinterval, yperiod = dinterval.get(interval, None)
            if yinterval == None : return None

            # determine start and end dates for data download 
            start = end.date() - timedelta(days=1) 
            print (f"{symbol} update required. {end} -> calculated start pos = {start}")

            # define new end target date. 
            # Note: data is downloaded till end date -1 *** ! IMPORTANT ! ***
            # end = end.date() + timedelta(days=2) # debug only 
            end = datetime.today().date() + timedelta(days=1)
            print (f"Downloading: start:{start} end:{end} for {symbol} w/ {yinterval} {yperiod}.")

            print ( f"Time Diff: { (datetime.today().date() - start).days } days" )
            if (datetime.today().date() - start).days > 60 and yinterval=='5m': 
                ## only for 5m data IF start date is beyond 60 days. 
                df = yf.download(tickers=symbol, interval=yinterval, period=yperiod)
                df.drop(df[(df.index.hour ==16) & (df.index.minute == 0)].index, inplace=True)  ## drop last row if it contains 16:00 hr data with 0 volume. 

            else : 
                df = yf.download(tickers=symbol, interval=yinterval, period=yperiod, start=start, end=end)

            df = fix_timezone(df)

            ######################      UPDATE and APPEND module    ###########################
                       
            dfdata = dfdata.append (df, ignore_index = False)  # appends data to previous data

            return dfdata

        else : ## if data is not outdated 
            print (f"No update required. Diff = {datetime.today().date() - end.date() } days")
            return dfdata
        ## assuming 

    else : 
        print (f"ERROR fetching symbol: {symbol}. Returned 0 rows. Check gatData() method")

    return dfdata



def updateDataEOD (watchlistName=None, interval='1H', persist=False) : 
    """ Update database end of day (EOD) data for 
        default (all): 1H, 1D, 4H, 5m intervals unless specified
        persists (to disk) : False (default)
    """
    
    # updateWatchlistLastUpdated() # update entire watchlist first 

    symbols = None 
    dfdata = None
    ddr = {}

    # select interval text for pickle names based on interval text alternatives 
    interval = finterval.get(interval, None)
    if interval == None : return None
    
    # select interval and period limits for yf download 
    yinterval, yperiod = dinterval.get(interval, None)
    if yinterval == None : return None

    # get the latest updated watchlist 
    watchlist = getWatchlist(watchlistName) # defaults to default watclist 
    symbols = watchlist.TICK.to_list()

    # find the start date : this is the min of last updated 'end.1H' for eg. columns 
    minDate = watchlist['end.'+interval].min() 
    maxDate = watchlist['end.'+interval].max() 
    start = minDate.date() - timedelta(days=1) 
    end = datetime.today().date() + timedelta(days=1)
    # end = maxDate.date() + timedelta(days=5)
    print ( f"Watchlist start={start} end={end}")
    
    symArray = list(chunks (symbols, 25))  # generate a list of symbol list of length 25 each 
    # print ( symArray)

    for symbols in symArray[:1]: 
        download = None
        print (f"downloading {symbols}")
        # start bulk download using yf
        if interval == '5m' :             
            download = yf.download(tickers=symbols, interval=yinterval, period=yperiod, group_by="Ticker")
        else: 
            download = yf.download(tickers=symbols, interval=yinterval, period=yperiod, start=start, end=end, group_by="Ticker")
        
        ## Update all the pickles 
        for symbol in symbols : 
            dfdata = getDataFromPickle(symbol, interval=interval)
            d = fix_timezone(download[symbol]) # extract Df from download and fixtimezone
            # Append to the existing dataframe 
            dfdata = pd.concat( (dfdata, d), axis=0)

            ddr[symbol] = dfdata  # append to local dict # debub only 
        
    return ddr
       


def chunks(mylist, n):    
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(mylist), n):
        yield mylist[i:i + n]




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
        print (f"Successful download : {symbol}, {interval}, {period}")
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
    """Reads all pickles to memory and return dictionary {symbol: dataframe}
    defaults: interval = 1H 
    """
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

## Helper 
def updateWatchlistLastUpdated(watchlistName=None, interval=None, symbol=None) : 
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

    if not interval and not symbol : # when not specified default = all     
        for interval in ['1H', '1D', '5m'] : 
            for symbol in symbols:  # load all data to memory 
                d = getData (symbol=symbol, interval=interval).dropna()
                start = d.index[0] # first datetime index 
                end = d.index[-1] # last datetime index 
                watchlist.loc[symbol, ['start.' + interval, 'end.' +interval]] = [start, end]  # update start and end time 
    
    elif symbol and not interval : 
        for interval in ['1H', '1D', '5m'] :             
            d = getData (symbol=symbol, interval=interval).dropna()
            start = d.index[0] # first datetime index 
            end = d.index[-1] # last datetime index 
            watchlist.loc[symbol, ['start.' + interval, 'end.' +interval]] = [start, end]  # update start and end time 
    
    elif symbol and interval : ## if single signal and interval is specified          
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

    


