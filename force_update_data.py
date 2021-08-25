"""
Script to Validate entire database.
All pickles will be rewritten. Backup data before use.
Use this with caution. This action cannot be reversed.
"""

import pandas as pd
from datetime import date
import app_web.logically.datasource as data
import random
import os.path, time


# ##  Agenda
# force Update to max allowed download limits 
# Update Daily close to [1H, 5m] close
# remove after and pre hours is any (need to think how to do this)  
# remove duplicates Resort database by index    


## Force Update all previous data to MAX downloadable values : numdays=None flag 
data.forceUpdateDataAll(numdays=None, watchlistName="WatchListLive.pickle", persist=True, chunksize=150)

# ## This will likely fail to download all at once
# data.forceUpdateDataAll(numdays=None, watchlistName="WatchListDBFull.pickle", persist=True)

## debug only 
# pp = data.forceUpdateDataAll(numdays=4, watchlistName="WatchListLive.pickle",persist=False)
# pp = data.forceUpdateData(numdays=2, watchlistName="WatchListLive.pickle", interval='5m')

# ## Generate 4H data 
# watchlist = data.getWatchlist(watchlistName="WatchListLive.pickle") # defaults to default watclist
# symbolslist = watchlist.TICK.to_list()
# for symbol in symbolslist :
#     data.gen4HdataFromPickle(symbol=symbol, persist=True)

# sort by time lastupdated and then generate list: to improve performance
## This operation cannot be reversed, use with caution!
data.force_sort_index_all(persist=True)

