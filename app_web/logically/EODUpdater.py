# This script is a blank updater for database
# Update intervals : 5m, 1H, 1D , 4H (resampled)
# Uses: df reduce_mem_usage before persist to disk - no active right now 


import yfinance as yf
import datasource as data

# test yf libs => functional 
# yf.download(tickers='SPY', interval='1h', period='200d').tail(50)  ## check additional
# yf.download(tickers='SPY', interval='1WK', period='200d').tail(20)  ## check additional


##############################
data.updateDataEODAll(watchlistName='WatchListDBFull.pickle', chunksize=100)

data.updateDataEODAll() # default watchlist 

data.updateDataEODAll(watchlistName='WatchListLive.pickle', chunksize=25) #default chunksize=25

#################################

## Test 
# data.getWatchlist(watchlistName='delistedWatchList.pickle')
#################################
