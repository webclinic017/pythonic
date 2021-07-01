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
    "1H"    : ("60m", "730d"),
    "1h"    : ("60m", "730d"),
    "H1"    : ("60m", "730d"),
    "h1"    : ("60m", "730d"),
    "1D"    : ("1d", "10000d"),
    "1d"    : ("1d", "10000d"),
    "d1"    : ("1d", "10000d"),
    "1WK"   : ("1WK", "10000d"),
    "WK"    : ("1WK", "10000d"),
    "W"     : ("1WK", "10000d"),
    "5m"    : ("5m", "60d"),
    "5M"    : ("5m", "60d"),
}
# used for file naming conventions
finterval = {
    "1H"    : "1H",
    "1h"    : "1H",
    "H1"    : "1H",
    "h1"    : "1H",
    "1D"    : "1D",
    "1d"    : "1D",
    "d1"    : "1D",
    "D1"    : "1D",
    "4H"    : "4H",
    "4h"    : "4H",
    "1WK"   : "1WK",
    "WK"    : "1WK",
    "W"     : "1WK",
    "5m"    : "5m",
    "5M"    : "5m",
}

### this is redundant at this time
def getData (symbol='SPY', interval='1H', dates=None, bars=None, period=None, days=None) : # only 1 symbol ata a time # download if does not exist

    # correct interval text alternatives for pickle names
    sinterval = finterval.get(interval, None)
    if sinterval == None : 
        print (f"{symbol} Interval {interval} not in database.")
        return None
    interval = sinterval
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
            if yinterval=='5m' :
                dfdata.drop(dfdata[(dfdata.index.hour ==16) & (dfdata.index.minute == 0)].index, inplace=True) ## drop last row if it contains 16:00 hr data with 0 volume for 5m.
            # pd.to_pickle(dfdata, flink)
            print ("Successful download : ", symbol, yinterval)
            # print (dfdata.head(10))
        else :
            print (symbol, yinterval, yperiod, 'ERROR!')
            return None
            # exit loop

    else : # read from pickle
        try:
            dfdata = pd.read_pickle(flink)
        except:
            print (f"Error Reading {flink} with for {symbol}{interval}")
            pass

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
        print (f"Symbol {symbol} not in database.")
        return None
        # exit loop
    else : # read from pickle
        dfdata = pd.read_pickle(flink)

    return dfdata.dropna()


def getTodayAll (symbolsList=None, dfdict=None, interval='1H', prepost=False, chunksize=25) : 
    """ Get todays Live data and append to dfdict 
        Assumption: data in dfdict is updated to previous EOD 
        No Time check will be included for performance reasons. 
        Preferable call after : loadtomemory() function to generate dict of symbols:DFs
    """
    if dfdict is None or symbolsList is None : 
        print ( "Argument Error. No dict provided.")
        return 
    
    # Start 
    start = datetime.today().date() # today only 

    symArray = list(chunks (symbolsList, chunksize))  # generate chunks of symbol list, length 25 each
    
    for symbols in symArray : # symArray[:1]
    
        # start bulk download using yf only for TODAY
        download = yf.download(tickers=symbols, interval=interval, start=start, group_by="Ticker", prepost=prepost)

        ## Update all the pickles
        for symbol in symbols :
            try :
                dfdata = dfdict[symbol]

                d = download[symbol].dropna() ## drop na from extracted df
                
                if len (d) > 0 :
                    d = fix_timezone(d) # extract Df from download and fixtimezone

                    # Append to the existing dataframe
                    dfdata = pd.concat( [dfdata, d])
                    dfdata = dfdata[~dfdata.index.duplicated(keep='last')] # remove duplicated by index
                    
                    dfdict[symbol] = dfdata  # append to local dict # debub only
            except:
                print (f"Error processing {symbol} {interval}")
                pass
    
    return dfdict


def getTodayOnly (symbolsList=None, interval='1H', prepost=False, chunksize=25) : 
    """ Get todays Live data of list of symbols and return dict of symbols:DFs
    """
    if symbolsList is None : 
        print ( "Argument Error. No symbols list provided.")
        return 
    
    dfdict = {} 
    # Start 
    start = datetime.today().date() # today only 

    symArray = list(chunks (symbolsList, chunksize))  # generate chunks of symbol list, length 25 each
    
    for symbols in symArray : # symArray[:1]
    
        # start bulk download using yf only for TODAY
        download = yf.download(tickers=symbols, interval=interval, start=start, group_by="Ticker", prepost=prepost)

        print (download.info(verbose=False, memory_usage="deep"))

        ## Update all the pickles
        for symbol in symbols :
            try :
                d = download[symbol].dropna() ## drop na from extracted df
                
                if len (d) > 0 :
                    d = fix_timezone(d) # extract Df from download and fixtimezone

                    # # Append to the existing dataframe
                    # dfdata = pd.concat( [dfdata, d])
                    # dfdata = dfdata[~dfdata.index.duplicated(keep='last')] # remove duplicated by index
                    
                    dfdict[symbol] = d  # append to local dict # debub only
            except:
                print (f"Error processing {symbol} {interval}")
                pass
    
    return dfdict




def downloadlastEODData (symbol='SPY', interval='1H', persist=True) : # only 1 symbol ata a time # download if does not exist

    # correct interval text alternatives for pickle names
    interval = finterval.get(interval, None)
    if interval == None : return None

    # generate the link to pickle file
    flink = TICKDATA + symbol+'.'+interval+'.pickle'
    # print (flink) # debug

    dfdata = None

    if not os.path.exists(flink) : # then download an save it
        print (f"Symbol {symbol} not in database. Downloading from internet.")

        for interval in ['1D', '1H', '5m'] : 

            # correct interval, period for text alternatives for yf.download
            yinterval, yperiod = dinterval.get(interval, None)
            if yinterval == None : return None

            print (f'Started download {symbol} for {yinterval} {yperiod}. ')
            end =  datetime.today().date() - timedelta(days=1)

            dfdata = yf.download(tickers=symbol, interval=yinterval, period=yperiod, end=end)
            if len(dfdata)>0  : # if successful download
                # fix timezone
                dfdata = fix_timezone(dfdata)
                if yinterval=='5m': ## drop last row if it contains 16:00 hr data with 0 volume for 5m.
                    dfdata.drop(dfdata[(dfdata.index.hour ==16) & (dfdata.index.minute == 0)].index, inplace=True)
                else : None 

                flink = TICKDATA + symbol+'.'+interval+'.pickle'
                pd.to_pickle(dfdata, flink) # save to disk as pickle

                print ("Successful download : ", symbol, yinterval, yperiod)
                # print (dfdata.head(10))
                if not inWatchlist(symbol=symbol) : 
                    addToWatchlist(symbols=[symbol])  # update watchlist with list of symbols in this case only one
            else :
                print (symbol, yinterval, yperiod, 'ERROR!')
                return None
                # exit loop

    else : # data pickle exists check each timeframe pickles, update each => persist to disk
        for interval in ['1D', '1H', '5m'] : 

            # correct interval, period for text alternatives for yf.download
            yinterval, yperiod = dinterval.get(interval, None)
            if yinterval == None : return None # else proceed to download & concat 

            dfdata = getDataFromPickle(symbol=symbol, interval=interval) # read pickle 
            end =  dfdata.index[-1]  # get last timestamp
            
            if end.date() < (datetime.today().date() - timedelta(days=1)) : 
                print (f"{symbol} Pickle update requred. end {end.date()} | today {datetime.today().date()}")
                start = end.date()
                end =  datetime.today().date() - timedelta(days=1)
                print (f"Downloading: start:{start} end:{end} for {symbol} w/ {yinterval} {yperiod}.")

                try: 
                    df = yf.download(tickers=symbol, interval=yinterval, period=yperiod, start=start, end=end)
                    print (df)

                    if len (df) > 0 :
                        df = fix_timezone(df) # extract Df from download and fixtimezone
                        # Append to the existing dataframe
                        dfdata = pd.concat( [dfdata, df])
                        dfdata = dfdata[~dfdata.index.duplicated(keep='last')] # remove duplicated by index

                        if yinterval=='5m': ## drop last row if it contains 16:00 hr data with 0 volume for 5m.
                            dfdata.drop(dfdata[(dfdata.index.hour ==16) & (dfdata.index.minute == 0)].index, inplace=True)

                        # Write to disk as pickle
                        flink = TICKDATA + symbol+'.'+interval+'.pickle'
                        if persist : pd.to_pickle(dfdata, flink)
                except:
                    print (f"Error processing {symbol} {interval}")
                    pass
            else:
                print (f"Data already uptodate lastEOD {symbol} {interval}")                

    print (f"Done downloading {symbol} all timeframes if no errors.")
    



def getupdatedData (symbol='SPY', interval='1H', watchlistName=None) :
    """ Append live data to pickle and show
        Will update symbol and return df to latest combining pickles and latest live
        !! this will NOT persist to disk
    """
    # only 1 symbol ata a time # download if does not exist to lates

    watchlist = getWatchlist(watchlistName) # defaults to default watclist
    symbols = watchlist.TICK.to_list()

    dfdata = getDataFromPickle(symbol=symbol, interval=interval)

    # print (dfdata)
    if dfdata is None:
        print (f"ERROR fetching symbol: {symbol}. Returned None.")

    elif len(dfdata) > 0  : # another check - df is valid and error free.

        # end =  pd.Timestamp(dfdata.index[-1]).to_pydatetime() # get last timestamp
        end =  dfdata.index[-1]  # get last timestamp

        print (f"End:{end}")

        if end.date() < datetime.today().date() : ## Update if data is outdated
            print ("DB outdated. Update started")

            ######################      DOWNLOAD  module    ###########################

            # correct interval, period for text alternatives for yf.download
            yinterval, yperiod = dinterval.get(interval, None)
            if yinterval == None : return None

            # determine start and end dates for data download
            start = end.date() # - timedelta(days=1)
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
                
                if len(df)>0: df.drop(df[(df.index.hour ==16) & (df.index.minute == 0)].index, inplace=True)  ## drop last row if it contains 16:00 hr data with 0 volume.

            else :
                df = yf.download(tickers=symbol, interval=yinterval, period=yperiod, start=start, end=end)

            df = fix_timezone(df) if len(df) > 0 else None
            print (df) # debug

            ######################      UPDATE and APPEND module    ###########################

            # Append to the existing dataframe
            dfdata = pd.concat( [dfdata, df])
            dfdata = dfdata[~dfdata.index.duplicated(keep='last')] # remove duplicated by index

            return dfdata

        else : ## if data is not outdated
            print (f"No update required. Diff = {datetime.today().date() - end.date() } days")
            return dfdata
        ## assuming

    else :
        print (f"ERROR fetching symbol: {symbol}. Returned 0 rows. Check gatData() method")

    return dfdata

########################    DATA CONSISTENCY CHECKER    ###########################

def dataConsistencyCheck (dfdata=None, interval=None ) : 
    if dfdata is None or interval is None: 
        print ("Invalid Argument Error. ")
        return 
    
    ## following define # entries per day 
    cinterval = {
        "1D"    : 1,
        "1d"    : 1,
        "1h"    : 7,
        "1H"    : 7,
        "4H"    : 2,
        "4h"    : 2,
        "5m"    : 78,
    }
    expCount = cinterval.get(interval, None) # expected count 
    if expCount is not None : print (f"Expected count: {expCount} per day") 
    else : return

    # check freq by day 
    anal = dfdata.groupby(pd.Grouper(freq='D')).count()    
    uniqlist=anal['Open'].unique().tolist()
    uniqlist.remove(0) # remove entries/days with no data 
    uniqlist.remove(expCount) # remove entries/days with expected data count 7 for 1h 
    
    flist = anal.loc[anal['Open'].isin(uniqlist)] # print the unique days 
    if len(flist) >0 : print (f"Found outlier data in df", flist)
    else: print (f"Data consistent.")




########################    MODULES FOR EOD DATABASE UPDATE    ###########################

def updateDataEODAll (watchlistName=None, persist=True) :
    """ Update database end of day (EOD) data for
    default (all): 1H, 1D, 4H, 5m intervals unless specified
    persists (to disk) : False (default)
    """
    for interval in ['1D', '1H', '5m'] :
        updateDataEOD (watchlistName=watchlistName, interval=interval, persist=persist)

    # Update data for interval = '4H'
    # get the latest updated watchlist
    watchlist = getWatchlist(watchlistName) # defaults to default watclist

    # sort by time lastupdated and then generate list: to improve performance
    symbolslist = watchlist.TICK.to_list()
    for symbol in symbolslist : 
        gen4HdataFromPickle(symbol=symbol, persist=True)

    print ( "**********     Data Update Complete.   ************" )
    sanitizeWatchlist(watchlistName=watchlistName, persist=persist)


def updateDataEOD (watchlistName=None, interval='1H', persist=True) :
    """ Update database end of day (EOD) data for
        default : 1H interval unless specified
        persists (to disk) : False (default)
    """

    updateWatchlistLastUpdated(watchlistName) # update entire watchlist first

    symbols = None
    dfdata = None
    ddr = {}

    # select interval text for pickle names based on interval text alternatives
    interval = finterval.get(interval, None)
    if interval == None :
        print (f"Bad interval {interval}")
        return None

    # select interval and period limits for yf download
    yinterval, yperiod = dinterval.get(interval, None)
    if yinterval == None : return None

    # get the latest updated watchlist
    watchlist = getWatchlist(watchlistName) # defaults to default watclist

    # sort by time lastupdated and then generate list: to improve performance
    symbolslist = watchlist.sort_values(by='end.'+interval, ascending=True).TICK.to_list()

    symArray = list(chunks (symbolslist, 25))  # generate a list of symbol list of length 25 each
    # print ( symArray)

    for symbols in symArray : # symArray[:1]
        download = None
        print (f"##\t\tDownloading {symbols}")

        # find the start date : this is the min of last updated 'end.1H' for eg. columns
        minDate = watchlist.loc[symbols]['end.'+interval].min()
        maxDate = watchlist.loc[symbols]['end.'+interval].max()
        start = minDate.date() - timedelta(days=1)
        end = datetime.today().date() + timedelta(days=1)
        # end = maxDate.date() + timedelta(days=5)
        print (f"Dates : min {minDate}, max {maxDate}")
        print ( f"Watchlist start={start} end={end}, interval: {interval}")

        # determine if ther is a need to update
        if minDate.date() < datetime.today().date() : ## Update if data us outdated
            print ("DB outdated. Update started")

            # start bulk download using yf
            if interval == '5m' :
                download = yf.download(tickers=symbols, interval=yinterval, period=yperiod, group_by="Ticker")
            else:
                download = yf.download(tickers=symbols, interval=yinterval, period=yperiod, start=start, end=end, group_by="Ticker")

            ## Update all the pickles
            for symbol in symbols :
                try :
                    dfdata = getDataFromPickle(symbol, interval=interval)
                    d = download[symbol].dropna() ## drop na from extracted df
                    if len (d) > 0 :
                        d = fix_timezone(d) # extract Df from download and fixtimezone
                        if yinterval=='5m': ## drop last row if it contains 16:00 hr data with 0 volume for 5m.
                            d.drop(d[(d.index.hour ==16) & (d.index.minute == 0)].index, inplace=True)
                        
                        # Append to the existing dataframe
                        dfdata = pd.concat( [dfdata, d])
                        dfdata = dfdata[~dfdata.index.duplicated(keep='last')] # remove duplicated by index
                        ddr[symbol] = dfdata  # append to local dict # debub only

                        # Write to disk as pickle
                        flink = TICKDATA + symbol+'.'+interval+'.pickle'
                        if persist : pd.to_pickle(dfdata, flink)
                except:
                    print (f"Error processing {symbol} {interval}")
                    pass
        else:
            print (f"DB already upto date | End Date {minDate.date()}. Skipping")

    return ddr  ## return dict of DFs



## break a bist into smaller chunks 
def chunks(mylist, n):
    """Yield successive n-sized chunks from a list."""
    for i in range(0, len(mylist), n):
        yield mylist[i:i + n]


def gen4HdataFromPickle (symbol=None, persist=False) :
    """Generates 4H resampled data from 1H pickles 
    """
    print (f"Generating 4H data for {symbol}")
    dfdata = generateResampledData(symbol=symbol, interval='4H', frominterval='1H', persist=persist)

    return dfdata


def generate4Hdata (inputDF=None) :
    """ This will resample input dataframe to 4H interval
        To be used for live resampling, does not persist data to disk
    """

    if inputDF is None : return None

    # interval = "4H"
        
    ## Resample to 4H timeframe
    aggregation = {
                'Open'  :'first',
                'High'  :'max',
                'Low'   :'min',
                'Close' :'last',
                'Volume':'sum'}
    dfdata = inputDF.resample('4H').agg(aggregation).dropna()

    return dfdata


def generateResampledData (symbol=None, interval='4H', frominterval='1H', persist=False) :
    """ This will resample to any to any interval
        input params: interfav (target sampling), frominterval (source data)
    """

    if symbol is None : return None
    dfdata = getDataFromPickle(symbol=symbol, interval=frominterval)
    if dfdata is None :
        print (f"{symbol} is incorrect/delisted/not-avaiable. Check source.")
        return None


    # interval = "4H"
    # Resampling Code
    ## Resample to 4H timefeame
    aggregation = {
                'Open'  :'first',
                'High'  :'max',
                'Low'   :'min',
                'Close' :'last',
                'Volume':'sum'}
    dfdata = dfdata.resample(interval).agg(aggregation).dropna()

    if persist :
        flink = TICKDATA + symbol+'.'+interval+'.pickle'
        pd.to_pickle(dfdata, flink) # save pickle to disk

    return dfdata




###########################################################################################


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


########################    MODULES FOR WATCHLIST MANAGEMENT    ###########################

def sanitizeWatchlist (watchlistName=None, oldDays=5, persist=False) :
    """ Removes symbols which are not updated beyond 5 days
    """

    watchlist = getWatchlist(watchlistName)
    delist = getWatchlist('delistedWatchList.pickle')

    df = watchlist[['end.1H']]
    value_counts = df.stack().value_counts() # Entire DataFrame
    threshold = 0.10*value_counts.sum() ## 10% of the total # of instruments
    to_remove = value_counts[value_counts <= threshold].index
    value_counts[value_counts <= 5].index
    fivedaysago = datetime.today().date() - timedelta(days=oldDays) # if older than 5 days
    pp = watchlist[watchlist['end.1H'].isin(to_remove)]['end.1H']
    removelist = pp[pp < fivedaysago].index
    print ( f"Symbol to remove (probably delisted): {removelist}")
    if len(removelist) == 0 :
        print ("No delisted symbol found. Nothing to remove. Quitting.")
        return

    delist = watchlist.loc[removelist] # add to delistwatchlist
    # print (delist)
    delistwatchList = getWatchlist('delistedWatchList.pickle')
    # print (delistwatchList, delist)
    delistwatchList = pd.concat([delistwatchList, delist]) ## add to watchlist
    delistwatchList = delistwatchList[~delistwatchList.index.duplicated(keep='last')] ## remove duplicates
    delistwatchList.to_pickle(DATAROOT+'delistedWatchList.pickle') ## persist to disk

    watchlist.drop(removelist, inplace = True) ## drop these from watchlist
    if persist : saveWatchlist(watchlist=watchlist, watchlistName=watchlistName)


def getWatchlist (watchlistName=None, interval='1H') :
    symbols = None

    if not watchlistName :
        # read default watchlist
        # read watchlist
        watchlistName = "WatchListDB.pickle"  # initialize

    watchlist = pd.read_pickle(DATAROOT + watchlistName ) # read file
    return watchlist



def showWatchlist (watchlistName=None, interval='1H') :
    """Describe frequency of a watchlist -> value counts
    """
    symbols = None

    if not watchlistName :
        # read default watchlist
        # read watchlist
        watchlistName = "WatchListDB.pickle"  # initialize

    watchlist = pd.read_pickle(DATAROOT + watchlistName ) # read file
    # print (watchlist)
    filter_col = [col for col in watchlist if col.startswith('end')]
    df = watchlist[filter_col]
    value_counts = df.stack().value_counts()
    print ("Listing Value Counts", value_counts)



def saveWatchlist (watchlist=None, watchlistName=None) :
    if (watchlist is not None) and (watchlistName is not None) :
        watchlist.to_pickle(DATAROOT+watchlistName)
        print (f"Saved Watchlist to {watchlistName}")

    elif (watchlist is not None) and (watchlistName is None) :
            # read default watchlist
            # read watchlist
            watchlistName = "WatchListDB.pickle"  # initialize
            watchlist.to_pickle(DATAROOT+watchlistName)
            print (f"Saved Watchlist to {watchlistName}")
    else :
        print ("ERROR Saving. Watchlist or WatchlistName not provided.")
        return


def addToWatchlist (symbols=None, watchlistName=None) :
    
    watchlistNames = []

    if not isinstance(symbols, list):
        print ("Symbols List expected NOT symbol. Quitting.")
        return 

    if watchlistName is None:
        # read default global watchlist
        watchlistNames = ["WatchListDBFull.pickle" ] # list of the default watchlist
    else : 
        watchlistNames = [watchlistName, "WatchListDBFull.pickle" ]
    
    print (f'Updating WatchList {watchlistNames} for {symbols}')

    for watchlistName in watchlistNames:
        watchlist = pd.read_pickle(DATAROOT + watchlistName ) # read file
        watchlist = watchlist.append(pd.DataFrame(symbols, columns=['TICK']), ignore_index=True)
        watchlist['id'] = watchlist['TICK']
        watchlist.set_index('id', inplace=True)  # prevent duplicates
        watchlist = watchlist[~watchlist.index.duplicated(keep='first')]
        print (watchlist.tail())

        saveWatchlist(watchlist, watchlistName=watchlistName) # save to disk 
        print (f"Added{symbols} to {watchlistName}")


def searchWatchlist (symbols=None, watchlistName=None) :
    """Search if symbol or list of symbols are in a watchlist
    """
    if not isinstance(symbols, list):
        print ("Symbols List expected NOT symbol. Quitting.")
        return 

    if watchlistName is None:
        watchlistName = "WatchListDB.pickle"  # initialize
    watchlist = pd.read_pickle(DATAROOT + watchlistName ) # read file
    flist = []
    for symbol in symbols :
        if symbol in watchlist.index.tolist() :
            flist.append(symbol)
    if len(flist) > 0:
        print (f"Watchlists query: {symbols} ", watchlist.loc[flist])
    else:
        print (f" {symbols} Not found")


def inWatchlist (symbol=None, watchlistName=None) :
    """Search if symbol or list of symbols are in a watchlist
    """
    if watchlistName is None:
        watchlistName = "WatchListDB.pickle"  # initialize
    watchlist = pd.read_pickle(DATAROOT + watchlistName ) # read file
    
    if symbol in watchlist.index.tolist() :    
        return True 
    else:
        # print (f" {symbols} Not found")
        return False


def loadDatatoMemory (watchlistName=None, interval='1H') :
    """Reads all pickles to memory and return dictionary {symbol: dataframe}
    defaults: interval = 1H
    """
    symbols = None

    if watchlistName is None:
        # read default watchlist
        # read watchlist
        watchlistName = 'WatchListDB.pickle'  # initialize
    print (f"Reading watchlist {watchlistName}")

    watchlist = pd.read_pickle(DATAROOT + watchlistName ) # read file
    symbols = watchlist.TICK.to_list()

    ddr = {} # define empty
    for symbol in symbols:  # load all data to memory
        try :
            ddr[symbol] = getDataFromPickle(symbol=symbol, interval=interval).dropna()
        except :
            print (f"Error reading symbolo {symbol}")
            pass

    return ddr, symbols


## new watchlist
def createWatchlist (watchlistName='DefaultWatchlist.pickle', symbols= None) :
    watchlist = pd.DataFrame(columns=['TICK', 'info' ])

    for symbol in symbols:
        watchlist=watchlist.append({
            'TICK' : symbol
        }, ignore_index=True)

    watchlist['id'] = watchlist['TICK']
    watchlist.set_index('id', inplace=True)  # prevent duplicates
    print (watchlist)
    watchlist.to_pickle(DATAROOT+watchlistName)
    return watchlist



## Helper
def updateWatchlistLastUpdated(watchlistName=None, interval=None, symbol=None) :
    """ Update watchlists with lastupdated column for interval : 1H, 1D, 4H, 5m
        column name format: start.<interval>
    """
    if watchlistName is None:
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
                d = getDataFromPickle (symbol=symbol, interval=interval).dropna()
                start = d.index[0] # first datetime index
                end = d.index[-1] # last datetime index
                watchlist.loc[symbol, ['start.' + interval, 'end.' +interval]] = [start, end]  # update start and end time

    elif symbol and not interval :
        for interval in ['1H', '1D', '5m'] :
            d = getDataFromPickle (symbol=symbol, interval=interval).dropna()
            start = d.index[0] # first datetime index
            end = d.index[-1] # last datetime index
            watchlist.loc[symbol, ['start.' + interval, 'end.' +interval]] = [start, end]  # update start and end time

    elif symbol and interval : ## if single signal and interval is specified
        d = getDataFromPickle (symbol=symbol, interval=interval).dropna()
        start = d.index[0] # first datetime index
        end = d.index[-1] # last datetime index
        watchlist.loc[symbol, ['start.' + interval, 'end.' +interval]] = [start, end]  # update start and end time

    #  Save watchlist to disk
    watchlist.to_pickle(DATAROOT+watchlistName)
    print (f"Successfully updated and saved watchlist {watchlistName} to disk")

    return watchlist

pd.options.mode.chained_assignment = None  ## Suppress copy slice warning

def fix_timezone (dfdata) : # for a single DF : dfdata
    """Timezone/ daylight saving fix for US instruments:
        get rid of -4:00 NY time added text
    """
    notfound = []
    dfdata['Datetime'] = dfdata.index
    dfdata['Datetime'] = dfdata['Datetime'].dt.tz_localize(None)
    dfdata.set_index('Datetime', inplace=True)

    return dfdata


def analyseDatabaseIntegrity () :
    pass

