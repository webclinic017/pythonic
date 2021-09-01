# This script is a blank updater for database
# Update intervals : 5m, 1H, 1D , 4H (resampled)
# Uses: df reduce_mem_usage before persist to disk - no active right now


import yfinance as yf
import datasource as data
from datetime import datetime, time

#####################Yahoo finance API TEST ######

# test yf libs => functional
print(yf.download(tickers='SPY', interval='1h', period='2d'))  ## check additional
print(yf.download(tickers='SPY', interval='1WK', period='1d').tail(8)) ## check additional
print(yf.download(tickers='SPY', interval='5m', period='1d').tail(8))  ## check additional


### First Update all watchlist
data.updateWatchlistLastUpdated(watchlistName='WatchListDBFull.pickle')
data.updateWatchlistLastUpdated(watchlistName='WatchListLive.pickle')
data.updateWatchlistLastUpdated() # DEFAULT watchlist

##############################
## Defaults
# chunksize=25, persist=False

# keep chunksize low (25 count) for consistency of downloads. 
data.updateDataEODAll(watchlistName='WatchListLive.pickle', chunksize=25, persist=True) #default chunksize=25

data.updateDataEODAll(chunksize=25, persist=True) # default watchlist

if time(0,0,0) <datetime.now().time() < time(4,0,0) : # if b.w midnight 00 AM to 4 AM
    print ("Scheduled full database download")
    data.updateDataEODAll(watchlistName='WatchListDBFull.pickle', chunksize=100, persist=True) ## update all database
else: 
    print ("Not downloading full. [outside download time range 0AM-4AM]")


#################################

## Test
# data.getWatchlist(watchlistName='delistedWatchList.pickle')
#################################
