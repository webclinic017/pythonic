# This script is a blank updater for database
# Update intervals : 5m, 1H, 1D , 4H (resampled)
# Uses: df reduce_mem_usage before persist to disk - no active right now 


import yfinance as yf
import datasource as data

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
data.updateDataEODAll(watchlistName='WatchListLive.pickle', chunksize=100, persist=True) #default chunksize=25

data.updateDataEODAll(chunksize=100, persist=True) # default watchlist 

# data.updateDataEODAll(watchlistName='WatchListDBFull.pickle', chunksize=100)



#################################

## Test 
# data.getWatchlist(watchlistName='delistedWatchList.pickle')
#################################
