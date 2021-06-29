## updater.py 
## This is an updater script to update datasource -> pd pickles in this case 


#### List of tasks 
##################################################
#   Update watchlist ->         add column last updated 
#   Update and Append EOD ->    data 1d, 1h, 5m, 4h: 1d (5 years), 1h (730 days), 5m (60 days) and 4h (downsampled); 
#                               read from watchlist, last updated values; fetch and append on new timestamps
#                               split symbols to download list -> bulk download splits and iterate -> symbol extraction -> fix timezones
#   


print ('Hello world')
